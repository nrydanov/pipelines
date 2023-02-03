import os
from importlib.util import spec_from_file_location, module_from_spec

import click

from pipelines.tasks import list_tasks

@click.group()
def cli():
  pass

@cli.command()
def run():
  spec = spec_from_file_location("pipeline", "pipeline.py")
  pipeline = module_from_spec(spec)
  spec.loader.exec_module(pipeline)
  pipeline.pipeline.run()

@cli.command()
def init():
  print(os.path.abspath(__file__))

@cli.command("tasks")
def available_tasks():
  lst = list_tasks()
  num = 1
  for (name, _) in lst:
    print(f"{num}. {name}")
    num += 1