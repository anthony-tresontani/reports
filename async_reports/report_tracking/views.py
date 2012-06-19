import copy
import shutil

from django.views.generic import ListView, DetailView
from django.http import HttpResponse

from .models import ReportTracking
from .report_handler import DjangoReportHandler
from . import get_report_by_name

# Create your views here.
class ReportTrackingView(ListView):
    model = ReportTracking
    template_name = "report_tracking/reports.html"
    context_object_name = "reports_list"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
       return  super(ReportTrackingView, self).get(request, *args, **kwargs)

    def post(self, request):
        data = copy.copy(request.POST)
        report_type = data.pop('report_action')[0]
        del data['csrfmiddlewaretoken']
        report_class = get_report_by_name(report_type)
        form_class = report_class.get_form_class()
        form = form_class(data)
        if not form.is_valid():
            self.invalid_form = form
            self.invalid_report_name = report_type
        else:
            report = report_class(report_handler=DjangoReportHandler(), parameters=form.clean_data)
            user = self.request.user if self.request.user.is_authenticated() else None
            report.produce(user=user)
        return self.get(request)

    def get_context_data(self, *args, **kwargs):
        context = super(ReportTrackingView, self).get_context_data(*args, **kwargs)
        if hasattr(self, "invalid_form"):
            context['invalid_form'] = self.invalid_form
            context['invalid_report_name'] = self.invalid_report_name
        return context

class ReportTrackingDetailView(DetailView):
    queryset = ReportTracking.objects.all()

    def get(self, request, *args, **kwargs):
        super(ReportTrackingDetailView, self).get(request, *args, **kwargs)
        response = HttpResponse(mimetype="text/csv")
        new_file = self.object.report_name + ' ' \
                   + str(self.object.report_date) + '.csv'
        response['Content-Disposition'] = 'attachment; filename=%s' % new_file
        file_ = open(self.object.report_file) 
        shutil.copyfileobj(file_, response)
        return response
