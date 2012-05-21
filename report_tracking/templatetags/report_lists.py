from django import template
from .. import report_lists

register = template.Library()

print "ID out", report_lists
@register.simple_tag(takes_context=True)
def available_reports(context):
    print "ID in", id(report_lists)
    context['available_reports'] = [report.name for report in report_lists]
    return ''
