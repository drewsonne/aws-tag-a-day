from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='aws-tag-a-day',
    version='0.1.1',
    packages=find_packages(exclude=('tests',)),
    description='A tool for simplifying swarming of fixing AWS tags',
    long_description_content_type='text/markdown',
    url='https://github.com/bliseng/aws-tag-a-day',
    license='Apache2',
    author='Drew J. Sonne',
    author_email='drew.sonne@gmail.com',
    install_requires=[
        'tabulate',
        'prompt_toolkit ',
        'hconf',
        'pyyaml'
    ],
    setup_requires=["pytest-runner","twine","wheel"],
    tests_require=["pytest"],
    entry_points={
        'console_scripts': [
            'tag-a-day = tag_a_day.cli:run'
        ],
        'tag_a_day.tag_handlers': [
            'ec2 = tag_a_day.services.ec2:EC2TagHandler',
            'rds = tag_a_day.services.rds:RDSTagHandler',
            's3 = tag_a_day.services.s3:S3TagHandler',
            'emr = tag_a_day.services.emr:EMRTagHandler',
        ]
    }
)
