import StringIO
import datetime
from htsql import HTSQL
from celery.task import task

from report_handler import ReportHandler
from formatter import CSVFormatter

from django.conf import settings
from django.forms import Form

class ReportMetaClass(type):
    def __new__(meta, classname, bases, classDict):
        cls = type.__new__(meta, classname, bases, classDict)
        abstract = hasattr(cls, "__abtract__") and cls.__abstract__
        if not cls.abstract():
            if not "name" in classDict:
                raise AttributeError("%s class should have a name" % classname)
        return cls


class Report(object):

    __metaclass__ = ReportMetaClass
    __abstract__ = True

    NO_RUN, RUNNING, DONE, FAILED = 0, 1, 2, -1
    status_description = {0: "No run",
                          1: "Running",
                          2: "Done",
                          -1: "Failed",
                          }

    def __init__(self, parameters=None, report_handler=ReportHandler()):
        self._data = []
        self.output = StringIO.StringIO()
        self.content = None
        self.asynchronous = getattr(self, "asynch", False)
        self.run = False
        self.report_handler = report_handler
        self.report_handler.add_report(self)
        self.status = self.NO_RUN
        self.parameters = parameters or {}

    @classmethod
    def abstract(cls):
        return getattr(cls, "__abstract__", False)

    @classmethod
    def get_verbose_name(self):
        return getattr(self, "verbose_name", self.name)

    def populate(self):
        raise NotImplementedError()

    def _populate(self, **kwargs):
       self.report_handler.pre_run(report=self, **kwargs)
       self.populate()
       self.post_populate()
       self.status = self.DONE
       self.report_handler.post_run(report=self, **kwargs)

    def _status(self):
        if not self.run:
            return self.NO_RUN
        if self.asynchronous:
            if self._status.ready():
                if self._status.successful():
                    return self.DONE
                else:
                    return self.FAILED
            else:
                return self.RUNNING
        else:
            return self.DONE

    def produce(self, **kwargs):
        self.run = True
        if self.asynchronous:
            async_populate.delay(self, **kwargs) 
            self.status = self.RUNNING
        else:
            self._populate(**kwargs)
        return self.status

    def get_data(self):
        header = self.get_header()
        if header:
            self.write_header(header)
        for line in self._data:
            self.write_line(line)
        self.content = self.output.getvalue()
        return self.content

    def post_populate(self):
        now_ = datetime.datetime.now().strftime("%Y%M%d_%H%m%s")
        self.filename = "/tmp/%s_%s_%d" % (self.name, now_,  id(self))
        self.as_file(self.filename)

    def as_file(self, filename):
        file_ = open(filename, "wb")
        if not self.content:
            self.get_data()
        file_.write(self.content)
        return file_

    def write_data(self, data):
        if not hasattr(self, "formatter"):
            self.formatter = CSVFormatter(self)
        if data:
            self.formatter.write([field.encode(getattr(self, "encoding", "utf8")) if hasattr(field, "encode") else field for field in data])

    def write_line(self, line):
        self.write_data(line)

    def get_header(self):
        return getattr(self, "header", [])

    def write_header(self, header):
        self.write_data(header)

    @classmethod
    def get_form_class(cls):
        return Form

    @classmethod
    def get_form(cls):
        if cls.get_form_class():
            return cls.get_form_class()()
        
@task
def async_populate(instance, **kwargs):
     instance._populate(**kwargs)

class HTSQLReport(Report):
    __abstract__ = True
    def __init__(self, *args, **kwargs):
        super(HTSQLReport, self).__init__(*args, **kwargs)
        self._connexion = getattr(self, "connexion", None) or getattr(settings,"HTSQL_REPORT_CONNEXION")

    def populate(self):
        # We can't store the session as there is no way to pickle it
        session = HTSQL(self._connexion)
        self._data = session.produce(self.query, **self.parameters)

class DjangoReport(Report):
    __abstract__ = True

    def populate(self):
        if hasattr(self, "get_queryset"):
            self._data = self.get_queryset()
        else:
            self._data = self.queryset

    def write_line(self, line):
        row = self.get_row(line)
        super(DjangoReport, self).write_line(row)

    def get_row(self, line):
        raise NotImplementedError()

