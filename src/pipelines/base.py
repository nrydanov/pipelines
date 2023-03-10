from sqlalchemy import (
  engine
)
from pydantic import (
  BaseSettings,
  PostgresDsn
)

class BaseTask:
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
  
  def description() -> None:
    pass