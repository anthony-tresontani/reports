report_lists = set()

def register(report_class):
    if report_class in report_lists:
        raise ValueError("Already registered report class %s" % report_class)
    report_lists.add(report_class) 

def get_report_by_name(name):
    report = filter(lambda report_class: report_class.name == name, report_lists)
    if report:
        return report[0]
    raise ValueError("No report %s registered" % name)
