import os

from pathlib import Path

import pandas as pd
from sqlalchemy import text

from pipelines.base import SqlTask

class ExecuteSql(SqlTask):
  def __init__(self, **kwargs) -> None:
    super().__init__()
    self.query = kwargs['query']
  
  def run(self) -> None:
    with self._engine.connect() as conn:
      conn.execute(text(self.query))
      conn.commit()
      
  def description(self):
    return f'{self.__class__.__name__}: {self.query}'
  
class SaveToFile(SqlTask):
  
  def __init__(self, **kwargs) -> None:
    super().__init__()
    self.input = kwargs['input']
    self.output = f"data/{kwargs['output']}"
    os.makedirs(Path(self.output).parent, exist_ok=True)
  
  def run(self) -> None:
    with self._engine.connect() as conn:  
      df = pd.read_sql(self.input, conn)
      df.to_csv(self.output)
      
  def description(self):
    return f'{self.__class__.__name__}: {self.input} -> {self.output}'

class LoadFileToDb(SqlTask):
  
  def __init__(self, **kwargs) -> None:
    super().__init__()
    self.input = f"data/{kwargs['input']}"
    self.output = kwargs['output']
  
  def run(self) -> None:
    df = pd.read_csv(self.input, sep=',')
    with self._engine.connect() as conn:
      conn.execute(text(f"DROP TABLE IF EXISTS {self.output}"))
      conn.commit()
      df.to_sql(self.output, self._engine)
      
  def description(self):
    return f'{self.__class__.__name__}: {self.input} -> {self.output}'
    
  
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
      
  def description(self):
    return f'{self.__class__.__name__}: {self.table}, {self.query}'