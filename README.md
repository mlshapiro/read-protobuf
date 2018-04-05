# read-protobuf

Import serialized protobuf directly into pandas DataFrame.

This is meant to be a simple shortcut to getting from serialized protobuf bytes / files directly to a dataframe. 

## Usage

```python
import demo_pb2                             # compiled protobuf message module 
from read_protobuf import read_protobuf

MessageType = demo_pb2.MessageType()        # instantiate a new message type
df = read_protobuf(b'\x00\x00', MessageType)    # create a dataframe from serialized protobuf bytes
df = read_protobuf([b'\x00\x00', b'x00\x00'] MessageType)    # read multiple protobuf bytes

df = read_protobuf('demo.pb', MessageType)    # use file instead of bytes
df = read_protobuf(['demo.pb', 'demo2.pb'], MessageType)    # read multiple files

# options
df = read_protobuf('demo.pb', MessageType, flatten=False)    # don't flatten pb messages
df = read_protobuf('demo.pb', MessageType, prefix_nested=True)    # prefix nested messages with parent keys (like pandas.io.json.json_normalize)
```

To compile a protobuf Message class from python, use:

```bash
$ protoc --python_out="." demo.proto
```

## Alternatives

### JSON

There are many alternatives to achieving this same goals including converting the message to JSON and then loading in pandas with `pd.read_json`.  

```python
from google.protobuf.json_format import MessageToJson
```

In my experience, this package is about twice as fast as converting through json. The process could be greatly improved by using c++ to do the processing.

### protobuf-to-dict

https://github.com/benhodgson/protobuf-to-dict

This library was developed earlier to convert protobufs to JSON via a dict.

## Develop

Currently developed for Python 3 using the anaconda python distribution. To install a development version of the package, run from the root directory:

```bash
$ pip install -e .
```

- To install development dependencies, use pip on the `dev-requirements.txt` file:

```bash
$ pip install -r dev-requirements.txt
```

## Lint

Uses `pylint` to lint application.

```
$ pylint read-protobuf
```

Configuration options are specified in `.pylintrc`

## Test

Uses `pytest` to run unit tests. From the root of the repository, run:

```
$ pytest
$ pytest -k "TestRead"    # only test the TestRead class
```

Configuration options are specified in `setup.cfg`

## Code Coverage

We use `coverage` to monitor code coverage during tests. To record coverage while running tests, run:

```bash
$ coverage run -m pytest        # watch files while testing
$ coverage report               # will display coverage report
```
