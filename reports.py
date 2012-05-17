import csv
import StringIO
from htsql import HTSQL

class Report(object):
    def __init__(self):
        self._data = []
        self.output = StringIO.StringIO()
        self.writer = csv.writer(self.output, delimiter=getattr(self, "delimiter", ","))
        self.content = None

    def produce(self):
        raise NotImplementedError()

    def write_line(self, line):
        self.writer.writerow([field.encode(getattr(self, "encoding", "utf8")) if hasattr(field, "encode") else field for field in line])

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
        
        

class HTSQLReport(Report):
    def __init__(self):
        super(HTSQLReport, self).__init__()
        self._session = HTSQL(self.connexion)

    def produce(self):
        self._data = self._session.produce(self.query)
