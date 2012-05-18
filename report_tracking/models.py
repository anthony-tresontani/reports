from django.db import models
from . import report_lists

# Create your models here.
class ReportTracking(models.Model):

    report_name = models.CharField(max_length=100)
    status = models.IntegerField(default=0)
    report_date = models.DateTimeField()

    class Meta:
        ordering = ["-report_date"]


    @classmethod
    def report_lists(cls):
        return [report.name for report in report_lists]
