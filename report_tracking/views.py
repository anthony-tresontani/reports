import copy
import shutil

from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from report_tracking.models import ReportTracking
from report_handler import DjangoReportHandler
from . import get_report_by_name

# Create your views here.
class ReportTrackingView(ListView):
    model = ReportTracking
    template_name = "report_tracking/reports.html"
    context_object_name = "reports_list"

    def post(self, request):
        data = copy.copy(request.POST)
        report_type = data.pop('report_action')[0]
        del data['csrfmiddlewaretoken']
        report_class = get_report_by_name(report_type)
        report = report_class(report_handler=DjangoReportHandler(), parameters=data)
        report.produce()
        return self.get(request)

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
