import os
from importlib.util import spec_from_file_location, module_from_spec
from shutil import copy2

import click

def get_pipeline():
  spec = spec_from_file_location("pipeline", "pipeline.py")
  pipeline = module_from_spec(spec)
  spec.loader.exec_module(pipeline)
  return pipeline

@click.group()
def cli():
  pass

@cli.command()
def run():
  pipeline = get_pipeline()
  pipeline.pipeline.run()

@cli.command()
def init():
  template_path = f"{os.path.dirname(__file__)}/template.py"
  cwd = f"{os.getcwd()}/pipeline.py"
  copy2(template_path, cwd)

@click.argument("path")  
@cli.command()
def add(path):
  if not os.path.exists("data/original"):
    os.makedirs("data/original")
  copy2(path, "data/original")

@cli.command("tasks")
def available_tasks():
  try:
    pipeline = get_pipeline()
    pipeline.pipeline.list_tasks()
  except FileNotFoundError:
    print('Error: No pipeline found in the current directory!')