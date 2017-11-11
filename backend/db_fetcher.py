# optional
import psycopg2

class DbFetcher:

  def __init__(self):
    # connect Postgres
    self.conn = None
    try:
      self.conn = psycopg2.connect("dbname='postgres' user='postgres' password=''")
    except:
      print("Error when connect to DB")
    self.cur = self.conn.cursor()

  def fetch(self, query):
    self.cur.execute(
      unicode("""
        SELECT query_data FROM query
        WHERE query = %(query)s"""),
      {"query": query})
    tokenized_text = self.cur.fetchone()
    return tokenized_text
