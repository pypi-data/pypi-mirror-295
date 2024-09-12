# setup.py
from setuptools import setup, find_packages

setup(
    name='data_quality_sdk',
    version='0.1.4',
    packages=find_packages(),
    install_requires=[
        'pyyaml',
        'kafka-python',
        'delta-spark',
        'pandas',
    ],
    description='A Data Quality SDK for real-time metrics and checks.',
    author='Suraj Chaudhary',
    author_email='suraj.chaudhary@xenonstack.com',
)
