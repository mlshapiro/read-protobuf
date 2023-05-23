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

#### MessageToJson

The google protobuf library comes with a utility to convert messages to JSON. 
The JSON objects could be loaded into pandas via `pd.read_json()`.

```python
from google.protobuf.json_format import MessageToJson
```

In brief tests, the `read_protobuf` package is about twice as fast
as using `MessageToJson`.

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
$ black read_protobuf.py tests/*.py
$ isort read_protobuf.py tests/*.py
```

## Lint

Uses `ruff` to lint application.

```bash
$ ruff read_protobuf.py
```

## Test

Uses `pytest` to run unit tests. From the root of the repository, run:

```bash
$ pytest
$ pytest -k "TestRead::test_read_bytes"    # specify test
```

## Code Coverage

Use `coverage` to monitor code coverage during tests.
To record coverage while running tests, run:

```bash
$ pytest --cov=read_protobuf
```

## License

[MIT License](LICENSE)
