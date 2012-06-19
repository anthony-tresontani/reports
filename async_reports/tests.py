from unittest import TestCase
from hamcrest import *
from async_reports.report import HTSQLReport, Report, DjangoReport
from async_reports.report_handler import MemoryReportHandler
from async_reports.report_tracking.report_handler import DjangoReportHandler
from async_reports.report_tracking.models import ReportTracking

class MyReportTest(HTSQLReport):
        encoding = "latin-1"
        query = "/school"
        delimiter = ";"
        connexion = "sqlite:htsql_demo.sqlite"
        name = "myReport"

class TestReport(TestCase):
    def setUp(self):
        self.report = MyReportTest()

    def test_synch_report(self):
        result = self.report.produce()
        content = self.report.get_data()
        file_report = self.report.as_file("/tmp/report.csv")
        assert_that(len(content.splitlines()), is_(18))
        assert_that(";" in content)
        assert_that(isinstance(file_report, file))

    def test_asynch_report(self):
        self.report.asynchronous = True
        result = self.report.produce()
        content = self.report.get_data()
        assert_that(self.report.status(), is_not(-1))
        assert_that(len(content.splitlines()), is_(18))

    def test_report_status(self):
        report_handler = MemoryReportHandler()
        report = MyReportTest(report_handler=report_handler)

        assert_that(len(report_handler.get_all_reports()), is_(1))
        assert_that(report_handler.get_all_reports()[0][0], none())

        report.produce()
        assert_that(report_handler.get_all_reports()[0][0], not_none())
        assert_that(report_handler.get_all_reports()[0][2], is_(Report.DONE))

    def test_header(self):
        report = MyReportTest()
        result = report.produce()
        content = report.get_data()
        assert_that(content.splitlines()[0], is_("art;School of Art & Design;old"))


class MyDjangoReportTest(DjangoReport):
    encoding = "latin-1"
    queryset = ReportTracking.objects.all()
    delimiter = ";"
    name = "my django report"

    def get_row(self, line):
        return [line.report_name, line.status]

class MyDjangoReportWithHeaderTest(MyDjangoReportTest):
    name = "my django report"
    header = ['report name', 'status']


class MyDjangoReportTest(DjangoReport):
    encoding = "latin-1"
    delimiter = ";"
    name = "my django report"

    def get_row(self, line):
        return [line.report_name, line.status]

    def get_queryset(self, **parameters):
        return ReportTracking.objects.all()

class DjangoReportTest(TestCase):
    def test_report(self):
        report = MyDjangoReportTest()
        result = report.produce()
        content = report.get_data()
        file_report = report.as_file("/tmp/report.csv")
        assert_that(len(content.splitlines()), is_(2))
        assert_that(";" in content)
        assert_that(isinstance(file_report, file))

    def test_report_with_header(self):
        report = MyDjangoReportWithHeaderTest()
        result = report.produce()
        content = report.get_data()
        file_report = report.as_file("/tmp/report.csv")
        assert_that(content.splitlines()[0], is_('report name;status'))


class DjangoReportHandlerTest(TestCase):
    def test_report_add_entries(self):
        report_handler = DjangoReportHandler()
        report = MyReportTest(report_handler=report_handler)
        report2 = MyReportTest(report_handler=report_handler)

        report.produce()
        assert_that(ReportTracking.objects.count(), is_(1))
        assert_that(ReportTracking.objects.all()[0].status, is_(Report.DONE))
