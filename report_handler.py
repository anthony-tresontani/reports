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
        self.report = report
        self.report_tracking, created = ReportTracking.objects.get_or_create(report_name=self.report.name,status=self.report.status(), report_date=date)

   def post_run(self, report):
       super(DjangoReportHandler, self).post_run(report)
       self.report_tracking.status = report.status()
       print "FILENAME", self.report.filename
       self.report_tracking.report_file = self.report.filename
       self.report_tracking.save()
