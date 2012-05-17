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
  HTSQL connexion