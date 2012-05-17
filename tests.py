from unittest import TestCase
from hamcrest import *
from reports import HTSQLReport

class TestReport(TestCase):
    class MyReport(HTSQLReport):
        encoding = "latin-1"
        query = "/school"
        delimiter = ";"
        connexion = "sqlite:htsql_demo.sqlite"

    def test_synch_report(self):
        report = TestReport.MyReport()
        result = report.produce()
        content = report.get_data()
        file_report = report.as_file("/tmp/report.csv")
        assert_that(len(content.splitlines()), is_(9))
        assert_that(";" in content)
        assert_that(isinstance(file_report, file))

    def test_asynch_report(self):
        report = TestReport.MyReport()
        report.asynchronous = True
        result = report.produce()
        content = report.get_data()
        assert_that(report.status(), is_not(-1))
        assert_that(len(content.splitlines()), is_(9))

