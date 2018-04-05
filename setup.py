"""
WzServer Setup
"""

from setuptools import setup

setup(
    name='read-protobuf',

    version='0.1.0',

    description='Small library to read serialized protobuf(s) directly into Pandas Dataframe',
    author='Marc Shapiro',
    url='https://github.com/mlshapiro/read-protobuf.git',
    license='Public Domain',
    keywords=['protobuf', 'pandas'],
    python_requires='>=3',
    install_requires=[
        'pandas>=0.16',
        'protobuf>=3.5'
    ],
    py_modules=['read_protobuf']
)
