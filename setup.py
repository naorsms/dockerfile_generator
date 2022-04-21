from setuptools import find_packages, setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='Dockerfile_generator',
    version='0.1.0',
    author='Naor Shemesh',
    author_email='naorsms96@gmail.com',
    decription='A utility for generate Dockerfile for ngnix-gunicorn-flask websites.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages=find_packages('src')
)