from pipelines.pipeline import Pipeline
import pipelines.tasks as tasks

NAME="project"
VERSION="0.1.0"

pipeline = Pipeline(NAME, VERSION, 
  tasks=[
    tasks.LoadFileToDb(
      input='original.csv',
      output='original'),
    tasks.CreateTableAs(
      table='norm',
      query=f'''
        select *, domain_of_url(url)
        from original;
      '''),
    tasks.SaveToFile(
      input='norm',
      output='norm'
    ),
    tasks.ExecuteSql(
      query=f'drop table original',
    ),
    tasks.ExecuteSql(
      query=f'drop table norm'
    )
  ]
)

pipeline.run()