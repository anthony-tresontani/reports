import copy

from django.views.generic import ListView
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
        report_class = get_report_by_name(report_type)
        report = report_class(report_handler=DjangoReportHandler())
        report.produce()
        return self.get(request)
