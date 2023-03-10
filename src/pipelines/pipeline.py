from datetime import datetime

class Pipeline:
  
  def __init__(self, name, version, tasks) -> None:
    self.name = name
    self.version = version
    self.tasks = tasks    
    
  def run(self):
    cnt = 1
    for task in self.tasks:
      print(f'Running task {cnt}')
      start = datetime.now()
      task.run()
      end = datetime.now()
      print(f'Task took {(end - start).total_seconds()} seconds')
      cnt += 1
      
  def list_tasks(self):
    print('Tasks:')
    for task in self.tasks:
      print(task.description())