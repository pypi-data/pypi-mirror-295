from setuptools import setup, find_packages
import os

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='peppers-spot-messaging',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['protobuf', 'grpcio'],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
