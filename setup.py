from setuptools import setup, find_packages
from pathlib import Path

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="jemawa",
    url="https://github.com/k1m0ch1/jemawa-menti-choices-spammer",
    author="k1m0ch1",
    version='1.1.0',
    description="Python CLI tool that spam the mentimeter live vote",
    packages=find_packages(),
    keywords='mentimeter menti spammer k1m0ch1',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email='yahya.kimochi@gmail.com',
    entry_points='''
    [console_scripts]
    jemawa=jemawa.cli:main
    ''',
    install_requires=[
        'art==5.1', 
        'beautifulsoup4==4.9.3',
        'certifi==2020.12.5',
        'progress==1.5',
        'requests==2.25.1'],
)
