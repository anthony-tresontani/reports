from django.db import models
from . import report_lists

# Create your models here.
class ReportTracking(models.Model):

    report_name = models.CharField(max_length=100)
    status = models.IntegerField(default=0)
    report_date = models.DateTimeField()
    report_file = models.FilePathField(null=True)

    class Meta:
        ordering = ["-report_date"]


    @classmethod
    def report_lists(cls):
        return [report.name for report in report_lists]

    def display_status(self):
        from report import Report
        return Report.status_description.get(self.status, "Invalid status") 

    def is_ready(self):
       from report import Report
       return self.status == Report.DONE

    def download(self):
       return "download"
