from setuptools import setup, find_packages

setup(
    name='pipelines',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'pipelines = cli:cli',
        ],
    },
)