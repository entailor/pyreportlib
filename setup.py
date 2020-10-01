import os
from setuptools import setup, find_packages

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='latexreport',
    version='0.1',
    description='pytailor report utilities',
    long_description=read('readme.MD'),
    url='http://www.entail.no',
    author='Entail AS',
    author_email='entail@entail.no',
    license='Proprietary',
    keywords='reporting preprocessing postprocessing',
    packages=find_packages(),
)
