"""
Test util.py methods
"""

import os
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

def write_demo_file():
    """Write demo pb file

    Returns:
        str: path to demo file
    """

    Message = write_demo()
    pwd = os.path.dirname(os.path.realpath(__file__))
    path = '{}/demo.pb'.format(pwd)

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
