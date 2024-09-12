from setuptools import setup, find_packages

setup(
    name='ecom_data_helpers_lib',
    version='0.0.9',
    description='A library of reusable utilities for AWS Lambda functions in ECOM Data Projects',
    author='Augusto Lorencatto',
    author_email='augusto.lorencatto@ecomenergia.com.br',
    packages=find_packages(),
    install_requires=[
        'boto3',
    ],
)