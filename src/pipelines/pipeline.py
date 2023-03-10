class Pipeline:
  
  def __init__(self, name, version, tasks) -> None:
    self.name = name
    self.version = version
    self.tasks = tasks    
    
  def run(self):
    for task in self.tasks:
      task.run()
      
  def list_tasks(self):
    for task in self.tasks:
      print(task.description())