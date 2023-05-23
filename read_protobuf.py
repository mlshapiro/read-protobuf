"""
read-protobuf

Small library to read serialized protobuf(s) directly into Pandas DataFrame
"""

from __future__ import annotations

from typing import Any

import google
import pandas as pd

DEFAULT_FLATTEN = True
DEFAULT_PREFIX_NESTED = False


def _to_array(
    message, flatten: bool, prefix_nested: bool, field: str = None
) -> list[dict[str, Any]]:
    """Convert an arbitrary message to an array

    Parameters
    ----------
    message : TYPE
        Description
    flatten : bool
        See `read_protobuf`
    prefix_nested : bool
        See `read_protobuf`
    field : str, optional
        Field within message to convert to array

    Returns
    -------
    list[dict[str, Any]]
        List of interpreted messages
    """
    if field:
        arr = [_interpret_message(m, flatten, prefix_nested) for m in getattr(message, field)]
    else:
        arr = [_interpret_message(message, flatten, prefix_nested)]

    return arr


def _interpret_message(message, flatten: bool, prefix_nested: bool) -> dict[str, Any]:
    """Interpret a message into a dict or array.

    Parameters
    ----------
    message : TYPE
        Description
    flatten : bool
        See `read_protobuf`
    prefix_nested : bool
        See `read_protobuf`

    Returns
    -------
    dict[str, Any]
    """

    data = {}  # default to dict
    for field in message.ListFields():
        # repeated nested message
        if field[0].type == field[0].TYPE_MESSAGE and field[0].label == field[0].LABEL_REPEATED:
            # is this the only field in the pb? if so, look at flatten
            if len(message.ListFields()) == 1 and flatten:
                data = _to_array(message, flatten, prefix_nested, field[0].name)

            # if there are multiple repeated messages in object, set as keys
            else:
                data[field[0].name] = _to_array(message, flatten, prefix_nested, field[0].name)

        # nested message
        elif field[0].type == field[0].TYPE_MESSAGE:
            if flatten:
                nested_dict = _interpret_message(field[1], flatten, prefix_nested)
                for key in nested_dict:
                    if key in data or prefix_nested:
                        data["{}.{}".format(field[0].name, key)] = nested_dict[key]
                    else:
                        data[key] = nested_dict[key]
            else:
                data[field[0].name] = _interpret_message(field[1], flatten, prefix_nested)

        # repeated scalar
        elif field[0].label == field[0].LABEL_REPEATED:
            data[field[0].name] = list(field[1])

        # scalar
        else:
            data[field[0].name] = field[1]

    return data


def read_protobuf(
    pb: str | bytes | list,
    MessageType: google.protobuf.message.Message,
    flatten: bool = DEFAULT_FLATTEN,
    prefix_nested: bool = DEFAULT_PREFIX_NESTED,
) -> pd.DataFrame:
    """Read protobuf file(s) or bytes into a Pandas DataFrame.

    Parameters
    ----------
    pb : string | bytes | list
        File path to pb file(s) or bytes from pb file(s).
        Multiple entries allowed in list.
    MessageType : google.protobuf.message.Message
        Message class of pb message
    flatten : bool, optional
        Flatten all nested objects into a 2-d dataframe.
        This will also collapse repeated message containers
    prefix_nested : bool, optional
        Prefix all flattened objects with parent keys

    Returns
    -------
    DataFrame
        Pandas DataFrame with interpreted pb data
    """

    # message parsing
    if not isinstance(pb, list):
        pb = [pb]

    raw = bytes()
    for entry in pb:
        if isinstance(entry, bytes):
            # python 2 interprets "bytes" as "str"
            # if the entry can be decoded as ascii, treat as a path
            try:
                entry.decode("ascii")
                with open(entry, "rb") as f:
                    raw += f.read()
            except (UnicodeDecodeError, AttributeError):
                raw += entry

        elif isinstance(entry, str):
            with open(entry, "rb") as f:
                raw += f.read()

        else:
            raise TypeError("unknown input source for protobuf")

    # parse concatenated message
    message = MessageType.FromString(raw)

    # check message
    if not message.ListFields():
        raise ValueError("Parsed message is empty")

    # intepret message
    data = _interpret_message(message, flatten, prefix_nested)

    # put data into frame
    return pd.DataFrame(data)
