"""
WzServer Setup
"""

from setuptools import setup

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='read-protobuf',
    version='0.1.1',
    description='Small library to read serialized protobuf(s) directly into Pandas Dataframe',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Marc Shapiro',
    url='https://github.com/mlshapiro/read-protobuf.git',
    license='Public Domain',
    keywords=['protobuf', 'pandas'],
    python_requires='>=2.7',
    install_requires=[
        'pandas>=0.16',
        'protobuf>=3.5'
    ],
    py_modules=['read_protobuf']
)
