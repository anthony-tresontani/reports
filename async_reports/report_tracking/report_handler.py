from async_messages import message_user
from async_reports.report_handler import ReportHandler
from .models import ReportTracking

class DjangoReportHandler(ReportHandler):
   def pre_run(self, report, **kwargs):
        super(DjangoReportHandler, self).pre_run(report)
        date, report, status = self.reports_exec[report]
        self.report = report
        self.report_tracking, created = ReportTracking.objects.get_or_create(report_name=self.report.get_verbose_name(),status=self.report.status, report_date=date)

   def post_run(self, report, **kwargs):
       super(DjangoReportHandler, self).post_run(report)

       user = kwargs.get("user", None)
       self.report_tracking.status = report.status
       self.report_tracking.report_file = self.report.filename
       self.report_tracking.data = self.report.parameters
       self.report_tracking.user = user
       self.report_tracking.save()

       if self.report_tracking.user:
           url = self.report_tracking.get_absolute_url()
           message_user(self.report_tracking.user, "Your report %s is ready <a href='%s'>here</a>" % (self.report.name, url))
