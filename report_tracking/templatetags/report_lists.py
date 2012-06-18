from django import template
from .. import report_lists

register = template.Library()

@register.simple_tag(takes_context=True)
def available_reports(context):
    context['available_reports'] = [(report.name, report.get_verbose_name(), report.get_form()) for report in report_lists]
    return ''
