from datetime import datetime

class ReportHandler(object):
    def __init__(self):
        self.reports_exec = {}

    def add_report(self, report):
        self.reports_exec[report] = (None, report, None)
    
    def pre_run(self, report, **kwargs):
        self.reports_exec[report] = (datetime.now(), report, None)

    def post_run(self, report, **kwargs):
        self.update_status(report)

    def update_status(self, report):
        date, report, status = self.reports_exec[report]
        self.reports_exec[report] = (date, report, report.status)

    def get_all_reports(self):
        for report in self.reports_exec:
            self.update_status(report)
        return self.reports_exec.values()

class MemoryReportHandler(ReportHandler):    
    pass
