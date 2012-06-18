from report import HTSQLReport, Report
from report_handler import MemoryReportHandler, DjangoReportHandler
from report_tracking.models import ReportTracking
from forms import *

class SchoolReport(HTSQLReport):
    encoding = "latin-1"
    query = "/department{name}?school.code=$sc"
    delimiter = ";"
    verbose_name = "school report"
    name = "school_report"

    @classmethod
    def get_form_class(self):
        return InputForm
            

class MyReport2(HTSQLReport):
    encoding = "latin-1"
    query = "/school"
    delimiter = ";"
    connexion = "sqlite:htsql_demo.sqlite"
    name= "async_report"
    async=True

    @classmethod
    def get_form_class(self):
        return IntegerInputForm
 
