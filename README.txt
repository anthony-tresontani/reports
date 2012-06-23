Let you build asynchronous report using any kind of engines like Django ORM or HTSQL.

Django-async-report try to solve the on request report.
When you build a reporting platform for you website, you will first synchronously write in the response the CSV content.
And your reports grow and grow and 2 minutes, a request lifecycle, is not anymore enough to calculate your report.

Want it asynchronous now, asynch=True. Done

Want also a report based on Django. Easy.

The report is stored on the server, your customer can download it again multiple times with recalculation.

Soon, more support to other formats.

Installation
------------

pip install django-async-reports

add 'async-reports.report_tracking' to INSTALLED_APPS

then run syncdb.

Be sure you have celery configured properly

If you want asynchronous message to be displayed when the report is completed, please install django-async-messages.

There is also a template example 

HTSQL Report creation
---------------

class MyReport(HTSQLReport):
    encoding = "latin-1"
    query = "/school"
    delimiter = ";"
    connexion = "sqlite:htsql_demo.sqlite"

`encoding`
  CSV file encoding

`query`
  HTSQL query

`delimiter`
  CSV delimiter

`connexion`
  HTSQL connexion. Can be defined sitewise with parameter HTSQL_CONNEXION

`asynch`
  Trigger the report asynchronously


Django Report creation
---------------
This example shows:
  - A django example
  - A report with a parameter selected through a custom form

class MyCustomForm(forms.Form):
    school_prefix = forms.CharField()

class MyReport(DjangoReport):
    encoding = "latin-1"
    delimiter = ";"
    header = ["school_name"]    

    def get_row(self, school):
        return [school.name]

    def get_queryset(self, school_prefix):
        return School.objects.filter(name__startswith=school_prefix)

    @classmethod
    def get_form_class:
        return MyCustomForm

`header`
  CSV file header

`queryset` or `get_queryset` function
  Return the list of element to be written in the report

`get_row(self, obj)`
  Transform an object in a list of value to be written in the report

`get_form_class`
  Return the custom form to be filled to generate the report with parameters.


Want the list of reports in a template
--------------------------------------

Use the `available_reports` templatetags


Want a template example
-----------------------

Use the one in async/templates/report_tracking
