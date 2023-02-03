import pandas as pd
import logging 

from sqlalchemy import (
  engine, text
)
from pydantic import (
  BaseSettings,
  PostgresDsn
)

class BaseTask:
  def __init__(self) -> None:
    self.logger = logging.getLogger()
  
  def run() -> None:
    pass

class SqlTask(BaseTask):
  class Settings(BaseSettings):
    pg_dsn: PostgresDsn
    
    class Config:
      env_file='.env'
      env_file_encoding = 'utf-8'
      
  def __init__(self) -> None:
    super().__init__()
      
    self.config = SqlTask.Settings().dict()
    self._engine = engine.create_engine(self.config['pg_dsn'])

  def run() -> None:
    pass

class ExecuteSql(SqlTask):
  def __init__(self, **kwargs) -> None:
    super().__init__()
    self.query = kwargs['query']
  
  def run(self) -> None:
    logging.info(f"Executing {self.query}")
    with self._engine.connect() as conn:
      conn.execute(text(self.query))
      conn.commit()
    logging.info(f"Finished executing {self.query}")
  
class SaveToFile(SqlTask):
  
  def __init__(self, **kwargs) -> None:
    super().__init__()
    self.input = kwargs['input']
    self.output = kwargs['output']
  
  def run(self) -> None:
    with self._engine.connect() as conn:  
      df = pd.read_sql(self.input, conn)
      df.to_csv(self.output)

class LoadFileToDb(SqlTask):
  
  def __init__(self, **kwargs) -> None:
    super().__init__()
    self.input = kwargs['input']
    self.output = kwargs['output']
  
  def run(self) -> None:
    df = pd.read_csv(self.input, sep=',')
    with self._engine.connect() as conn:
      conn.execute(text(f"DROP TABLE IF EXISTS {self.output}"))
      conn.commit()
      df.to_sql(self.output, self._engine)
    
  
class CreateTableAs(SqlTask):
  
  def __init__(self, **kwargs) -> None:
    super().__init__()
    self.table = kwargs['table']
    self.query = kwargs['query']
  
  def run(self) -> None:
    with self._engine.connect() as conn:
      conn.execute(text(f"DROP TABLE IF EXISTS {self.table}"))
      sql = f'''
        CREATE TABLE {self.table} AS 
          {self.query}
      '''
      conn.execute(text(sql))
      conn.commit()