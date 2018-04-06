# read-protobuf

Small library to read serialized protobuf(s) directly into Pandas Dataframe.

This is meant to be a simple shortcut to getting from serialized protobuf bytes / files directly to a dataframe.

>Note: This currently only supports basic proto3 features for Python 3. I have not yet tested it with proto2, though I believe that should work. I plan to expand the utility of this library with time and need.

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

#### JSON

The google protobuf library comes with a utility to convert messages to JSON. Then the JSON objects could be loaded into pands via `pd.read_json()`.  

```python
from google.protobuf.json_format import MessageToJson
```

In my brief tests, the `read_protobuf` package is about twice as fast as converting a protobuf to a dataframe using `MessageToJson`. 

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
$ pylint read_protobuf
```

Configuration options are specified in `.pylintrc`

## Test

Uses `pytest` to run unit tests. From the root of the repository, run:

```
$ pytest
$ pytest -k "TestRead::test_read_bytes"    # specify test
```

Configuration options are specified in `setup.cfg`

## Code Coverage

We use `coverage` to monitor code coverage during tests. To record coverage while running tests, run:

```bash
$ coverage run -m pytest        # watch files while testing
$ coverage report               # will display coverage report
```


## UnLicense

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>


