# read-protobuf

Import protobufs directly into pandas dataframe

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
