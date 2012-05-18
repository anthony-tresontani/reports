from datetime import datetime
from report_tracking.models import ReportTracking

class ReportHandler(object):
    def __init__(self):
        self.reports_exec = {}

    def add_report(self, report):
        self.reports_exec[report] = (None, report, None)
    
    def pre_run(self, report):
        self.reports_exec[report] = (datetime.now(), report, None)

    def post_run(self, report):
        self.update_status(report)

    def update_status(self, report):
        date, report, status = self.reports_exec[report]
        self.reports_exec[report] = (date, report, report.status())

    def get_all_reports(self):
        for report in self.reports_exec:
            self.update_status(report)
        return self.reports_exec.values()

class MemoryReportHandler(ReportHandler):    
    pass

class DjangoReportHandler(ReportHandler):
   def pre_run(self, report):
        super(DjangoReportHandler, self).pre_run(report)
        date, report, status = self.reports_exec[report]
        report_track = ReportTracking.objects.get_or_create(report_name="name",status=0, report_date=date)

   def post_run(self, report):
       super(DjangoReportHandler, self).post_run(report)
       report_tracking = ReportTracking.objects.get(report_name="name")
       report_tracking.status = report.status()
       report_tracking.save()
