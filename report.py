import StringIO
from htsql import HTSQL
from celery.task import task

from report_handler import ReportHandler
from formatter import CSVFormatter

class ReportMetaClass(type):
    def __new__(meta, classname, bases, classDict):
        cls = type.__new__(meta, classname, bases, classDict)
        if not classname in ["Report", "HTSQLReport"]:
            if not "name" in classDict:
                raise AttributeError("%s class should have a name" % classname)
        return cls


class Report(object):

    __metaclass__ = ReportMetaClass

    NO_RUN, RUNNING, DONE, FAILED = 0, 1, 2, -1

    def __init__(self, report_handler=ReportHandler(), formatter=CSVFormatter):
        self._data = []
        self.output = StringIO.StringIO()
        self.formatter = formatter(self)
        self.content = None
        self.asynchronous = getattr(self, "asynch", False)
        self.run = False
        self.report_handler = report_handler
        self.report_handler.add_report(self)
        self._status = None

    def populate(self):
        raise NotImplementedError()

    def status(self):
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

    def produce(self):
        self.run = True
        self.report_handler.pre_run(report=self)
        if self.asynchronous:
            self._status = async_populate.delay(self) 
        else:
            self.populate()
        self.report_handler.post_run(report=self)
        return self.status()

    def write_line(self, line):
        self.formatter.write([field.encode(getattr(self, "encoding", "utf8")) if hasattr(field, "encode") else field for field in line])

    def get_data(self):
        for line in self._data:
            self.write_line(line)
        self.content = self.output.getvalue()
        return self.content

    def as_file(self, filename):
        file_ = open(filename, "wb")
        if self.content:
            file_.write(self.content)
            return file_
        
@task
def async_populate(instance):
     return instance.populate()
        

class HTSQLReport(Report):
    def __init__(self, *args, **kwargs):
        super(HTSQLReport, self).__init__(*args, **kwargs)
        self._session = HTSQL(self.connexion)

    def populate(self):
        self._data = self._session.produce(self.query)