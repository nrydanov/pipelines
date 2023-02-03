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
            output='norm',
        ),

        # clean up:
        ExecuteSql('drop table original'),
        ExecuteSql('drop table norm'),
    ]
)