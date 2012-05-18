from report import HTSQLReport, Report
from report_handler import MemoryReportHandler, DjangoReportHandler
from report_tracking.models import ReportTracking

class MyReport(HTSQLReport):
    encoding = "latin-1"
    query = "/school"
    delimiter = ";"
    connexion = "sqlite:htsql_demo.sqlite"
    name= "my name"

