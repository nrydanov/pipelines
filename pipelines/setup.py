from setuptools import setup

setup(
    name='pipelines',
    version='0.1.0',
    py_modules=['pipelines'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'pipelines = pipelines:pipelines',
        ],
    },
)