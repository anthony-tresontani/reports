Let you build asynchronous report using any kind of engines like Django ORM or HTSQL.

Report creation
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
