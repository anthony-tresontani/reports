import os
from django.db import models
from django.contrib.auth.models import User
from . import report_lists

# Create your models here.
class ReportTracking(models.Model):

    report_name = models.CharField(max_length=100)
    status = models.IntegerField(default=0)
    report_date = models.DateTimeField()
    report_file = models.FilePathField(null=True)
    user = models.ForeignKey(User, blank=True, null=True)

    class Meta:
        ordering = ["-report_date"]


    @classmethod
    def report_lists(cls):
        return [report.name for report in report_lists]

    def display_status(self):
        from report import Report
        return Report.status_description.get(self.status, "Invalid status") 

    def is_file_ready(self):
       from report import Report
       return self.status == Report.DONE and os.path.exists(self.report_file)

    def download(self):
       return "download"

    @models.permalink
    def get_absolute_url(self):
        pass
