# Pipelines — ETL Framework

## Quickstart

### Initialization

Create a new folder and run `pipelines init` inside of it.

It will create a file named `pipeline.py` with the following content:

```python
from pipelines.pipeline import Pipeline
from pipelines.tasks import LoadFileToDb, CreateTableAs, SaveToFile, ExecuteSql

NAME = 'test_project'
VERSION = "0.1.0"

pipeline = Pipeline(
    name=NAME,
    version=VERSION,
    tasks=[
        LoadFileToDb(
            input='original/original.csv',
            output='original',
        ),
        CreateTableAs(
            table='norm',
            query='''
                select *, domain_of_url(url)
                from original;
            '''
        ),
        SaveToFile(
            input='norm',
            output='norm/norm.csv',
        ),

        # clean up:
        ExecuteSql(query='drop table original'),
        ExecuteSql(query='drop table norm'),
    ]
)
```

The idea of this pipeline is to load the existing file with URLs and normalize them — extract domain name for each url, and finally save the result back to CSV-file.

### List available tasks


```shell
> pipelines tasks
Tasks:
LoadFileToDb: data/original/original.csv -> original
CreateTableAs: norm, 
                select *, domain_of_url(url)
                from original;
            
SaveToFile: norm -> data/norm/norm.csv
ExecuteSql: drop table original
ExecuteSql: drop table norm
```

### Add files

Let's create file `original.csv` somewhere with the following content:

```csv
id,name,url
1,hello,http://hello.com/home
2,world,https://world.org/
```

Formatted:

id |  name | url
-- | ----- | ---
 1 | hello | http://hello.com/home
 2 | world | https://world.org/

Now you can add it to your data sources using following command:

```shell
> pipelines add original.csv
```

### Running the pipeline

```shell
> pipeline tasks
Error: No pipeline found in the current directory!

> cd test_project
> pipeline tasks
Tasks:
LoadFileToDb: data/original/original.csv -> original
CreateTableAs: norm, 
                select *, domain_of_url(url)
                from original;
            
SaveToFile: norm -> data/norm/norm.csv
ExecuteSql: drop table original
ExecuteSql: drop table norm
```

Now, when we have all the dependencies in place, we can run the pipeline using `pipelines run`.

```shell
> pipelines run
Running task 1
Task took 0.07383 seconds
Running task 2
Task took 0.06311 seconds
Running task 3
Task took 0.060276 seconds
Running task 4
Task took 0.023472 seconds
Running task 5
Task took 0.022453 seconds
```

### Results

You can see the result of you work in `data/norm.csv.gz`.

```csv
id,name,url,domain_of_url
1,hello,http://hello.com/home,hello.com
2,world,https://world.org/,world.org
```

Formatted:

id |  name |                   url | domain_of_url
-- | ----- | --------------------- | -------------
 1 | hello | http://hello.com/home | hello.com
 2 | world |    https://world.org/ | world.org
