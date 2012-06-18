import csv

class CSVFormatter(object):
    def __init__(self, report):
        self.report = report
        self.delimiter = getattr(self.report, "delimiter", ";")
        self.writer = csv.writer(self.report.output, delimiter=self.delimiter)

    def write(self, line):
        self.writer.writerow(line)
