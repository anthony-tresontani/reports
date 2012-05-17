from unittest import TestCase
from hamcrest import *
from reports import HTSQLReport

class TestReport(TestCase):

    def test_report(self):
        class MyReport(HTSQLReport):
            encoding = "latin-1"
            query = "/school"
            delimiter = ";"
            connexion = "sqlite:htsql_demo.sqlite"

        report = MyReport()
        result = report.produce()
        content = report.get_data()
        file_report = report.as_file("/tmp/report.csv")
        assert_that(len(content.splitlines()), is_(9))
        assert_that(";" in content)
        assert_that(isinstance(file_report, file))

