from prefect import flow,task
from prefect_sqlalchemy import SqlAlchemyConnector, SyncDriver, ConnectionComponents
import pandas as pd

@task
def load_file_to_db(input, output):
  df = pd.read_csv(input, sep=',')
  print(df)
  with SqlAlchemyConnector(
    connection_info=ConnectionComponents(
      driver=SyncDriver.POSTGRESQL_PSYCOPG2,
      database='orion',
      username='sa',
      password='1234',
      host='localhost,5432'
    ),
  ) as db:
    db.execute(f"DROP TABLE IF EXISTS {output}")
    df.to_sql(output, db._engine, )
      

@task
def sql_create_table_as(table, query):
   with SqlAlchemyConnector(
    connection_info=ConnectionComponents(
      driver=SyncDriver.POSTGRESQL_PSYCOPG2,
      database='orion',
      username='sa',
      password='1234',
      host='localhost,5432'
    ),
  ) as db:
    db.execute(f"DROP TABLE IF EXISTS {table}")
    sql = f'''
    CREATE TABLE {table} AS
      {query}
    '''
    db.execute(sql)

@task
def save_table_to_file(input, output):
  with SqlAlchemyConnector(
    connection_info=ConnectionComponents(
      driver=SyncDriver.POSTGRESQL_PSYCOPG2,
      database='orion',
      username='sa',
      password='1234',
      host='localhost,5432'
    ),
  ) as db:
    df = pd.read_sql(input, db._engine)
    print(df)
    df.to_csv(output)

INPUT="test.csv"
OUTPUT="norm.csv"

@flow
def run_pipeline(filepath):
  load_file_to_db(filepath, 'original')
  sql_create_table_as('norm', '''
    SELECT *, domain_of_url(URL)
    FROM original;                
  ''')
  save_table_to_file('norm', OUTPUT)
  
  
if __name__ == '__main__':
  run_pipeline(INPUT)
