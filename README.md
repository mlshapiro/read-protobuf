# read-protobuf

Small library to read serialized protobuf(s) directly into Pandas DataFrame.

This is intended to be a simple shortcut for translating serialized
protobuf bytes / files directly to a dataframe.

## Install

Available via pip:

```bash
$ pip install read-protobuf
```

## Usage

Run the [demo-notebook](tests/demo.ipynb) for an interactive demo.

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

#### protobuf-to-dict

https://github.com/benhodgson/protobuf-to-dict

This library was developed earlier to convert protobufs to JSON via a dict.

#### MessageToDict, MessageToJson

The google protobuf library comes with utilities to convert messages to a `dict` or JSON,
then loaded by Pandas.

```python
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import MessageToDict
```

In brief tests, the `read_protobuf` package is about 2x as fast
as using `MessageToDict` and 3x as fast as `MessageToJson`.

## Develop

To install a development version of the package, run from the root directory:

```bash
$ pip install -e .
```

- To install development dependencies, use the optional `[dev]`dependencies:

```bash
$ pip install -e ".[dev]"
```

## Format

Uses `black` and `isort` to format files.

```bash
$ make black
$ make isort
```

## Lint

Uses `ruff` to lint application.

```bash
$ make ruff
```

## Test

Uses `pytest` to run unit tests. From the root of the repository, run:

```bash
$ make pytest

# specify test
$ pytest -k "TestRead::test_read_bytes"
```

## Code Coverage

Use `coverage` to monitor code coverage during tests.
To record coverage while running tests, run:

```bash
$ make pytest-cov
```

## License

[MIT License](LICENSE)
