from unittest import TestCase
from hamcrest import *
from report import HTSQLReport, Report
from report_handler import MemoryReportHandler, DjangoReportHandler
from report_tracking.models import ReportTracking

class MyReportTest(HTSQLReport):
        encoding = "latin-1"
        query = "/school"
        delimiter = ";"
        connexion = "sqlite:htsql_demo.sqlite"
        name = "myReport"
        arguments = ['name']

class TestReport(TestCase):
    def test_synch_report(self):
        report = MyReport()
        result = report.produce()
        content = report.get_data()
        file_report = report.as_file("/tmp/report.csv")
        assert_that(len(content.splitlines()), is_(9))
        assert_that(";" in content)
        assert_that(isinstance(file_report, file))

    def test_asynch_report(self):
        report = MyReport()
        report.asynchronous = True
        result = report.produce()
        content = report.get_data()
        assert_that(report.status(), is_not(-1))
        assert_that(len(content.splitlines()), is_(9))

    def test_report_status(self):
        report_handler = MemoryReportHandler()
        report = MyReport(report_handler=report_handler)

        assert_that(len(report_handler.get_all_reports()), is_(1))
        assert_that(report_handler.get_all_reports()[0][0], none())

        report.produce()
        assert_that(report_handler.get_all_reports()[0][0], not_none())
        assert_that(report_handler.get_all_reports()[0][2], is_(Report.DONE))

class DjangoReportHandlerTest(TestCase):

    def test_report_add_entries(self):
        report_handler = DjangoReportHandler()
        report = MyReport(report_handler=report_handler)
        report2 = MyReport(report_handler=report_handler)

        report.produce()
        assert_that(ReportTracking.objects.count(), is_(1))
        assert_that(ReportTracking.objects.all()[0].status, is_(Report.DONE))
