from report import HTSQLReport, Report
from report_handler import MemoryReportHandler, DjangoReportHandler
from report_tracking.models import ReportTracking
from forms import InputForm

class SchoolReport(HTSQLReport):
    encoding = "latin-1"
    query = "/department{name}?school.code=$school_code"
    delimiter = ";"
    connexion = "sqlite:htsql_demo.sqlite"
    name = "school report"

    @classmethod
    def get_form_class(self):
        return InputForm
            

class MyReport2(HTSQLReport):
    encoding = "latin-1"
    query = "/school"
    delimiter = ";"
    connexion = "sqlite:htsql_demo.sqlite"
    name= "report2"

