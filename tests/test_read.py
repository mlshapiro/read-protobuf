"""
Test util.py methods
"""

import os
import pytest
import pandas as pd
from read_protobuf import read_protobuf

from . import demo_pb2


def write_demo(n=100):
    """Write demo pb string

    Args:
      n (int, optional): number of entries in the demo pb record

    Returns:
      byte-string: serialized pb string
    """

    Collection = demo_pb2.Collection()
    Record = demo_pb2.Record()

    Record.int = 1234
    Record.float = 43.685
    Record.nested.data = 1.2        #pylint: disable=E1101
    Record.rep.extend([1])          #pylint: disable=E1101
    Record.rep.extend([2])          #pylint: disable=E1101

    RecordTwo = demo_pb2.Record()
    RecordTwo.int = 1253135
    RecordTwo.float = -73.2324

    # add both types of records at random
    for i in range(n):
        if i % 5 == 0:
            Collection.records.extend([RecordTwo])  #pylint: disable=E1101
        else:
            Collection.records.extend([Record]) #pylint: disable=E1101

    return Collection.SerializeToString()

def write_demo_file(name='demo.pb'):
    """Write demo pb file

    Returns:
        str: path to demo file
    """

    Message = write_demo()
    pwd = os.path.dirname(os.path.realpath(__file__))
    path = '{}/{}'.format(pwd, name)

    with open(path, 'wb') as f:
        f.write(Message)

    return path


class TestRead(object):
    """Test read-protobuf methods"""

    def test_read_bytes(self):
        """test input serialized bytes"""

        Message = write_demo()
        Collection = demo_pb2.Collection()
        df = read_protobuf(Message, Collection)

        assert df is not None and isinstance(df, pd.DataFrame)


    def test_read_file(self):
        """test input file path"""

        path = write_demo_file()
        Collection = demo_pb2.Collection()
        df = read_protobuf(path, Collection)

        assert df is not None and isinstance(df, pd.DataFrame)

    def test_defaults(self):
        """test default inputs"""

        Message = write_demo()
        Collection = demo_pb2.Collection()

        df = read_protobuf(Message, Collection)

        assert 'data' in df.columns

    def test_flatten(self):
        """test flatten option"""

        Message = write_demo()
        Collection = demo_pb2.Collection()

        df = read_protobuf(Message, Collection, flatten=False)

        assert 'records' in df.columns and len(df.columns) == 1

    def test_prefix(self):
        """test prefix option"""

        Message = write_demo()
        Collection = demo_pb2.Collection()

        df = read_protobuf(Message, Collection, prefix_nested=True)

        assert 'nested.data' in df.columns

    def test_multiple_input_bytes(self):
        """test input multiple bytes"""

        Message = write_demo(n=29)
        Message2 = write_demo(n=5)

        Collection = demo_pb2.Collection()

        df = read_protobuf([Message, Message2], Collection)

        assert df is not None and isinstance(df, pd.DataFrame)

    def test_multiple_input_files(self):
        """test input multiple files"""

        path1 = write_demo_file()
        path2 = write_demo_file('demo2.pb')

        Collection = demo_pb2.Collection()

        df = read_protobuf([path1, path2], Collection)

        assert df is not None and isinstance(df, pd.DataFrame)


    def test_multiple_input_types(self):
        """test input multiple files and strings"""

        Message = write_demo(n=29)
        path2 = write_demo_file('demo2.pb')

        Collection = demo_pb2.Collection()

        df = read_protobuf([Message, path2], Collection)

        assert df is not None and isinstance(df, pd.DataFrame)

    def test_invalid_pb(self):
        """test invalid pb class"""

        Message = write_demo()
        Collection = demo_pb2.Collection()

        Record = demo_pb2.Record()
        Record.int = 1234
        Record.float = 43.685
        Message2 = Record.SerializeToString()

        df = read_protobuf([Message, Message2], Collection)

        assert df is not None and isinstance(df, pd.DataFrame)

        with pytest.raises(ValueError):
            df = read_protobuf([Message2], Collection)

    def test_invalid_input_path(self):
        """test invalid input filepath"""

        Collection = demo_pb2.Collection()

        with pytest.raises(IOError):
            read_protobuf('message', Collection)

    def test_invalid_input(self):
        """test invalid input pb type"""

        Collection = demo_pb2.Collection()

        with pytest.raises(TypeError):
            read_protobuf(123, Collection)
