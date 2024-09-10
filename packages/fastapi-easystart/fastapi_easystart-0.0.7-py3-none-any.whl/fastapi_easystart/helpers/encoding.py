import datetime
import gzip
import io
import json
from decimal import Decimal
from typing import Optional, Dict, Any

_PROTECTED_TYPES = (
    type(None),
    int,
    float,
    Decimal,
    datetime.datetime,
    datetime.date,
    datetime.time,
)


class CustomUnicodeDecodeError(UnicodeDecodeError):
    def __init__(self, obj, *args):
        self.obj = obj
        super().__init__(*args)

    def __str__(self):
        return "%s. You passed in %r (%s)" % (
            super().__str__(),
            self.obj,
            type(self.obj),
        )


def is_protected_type(obj):
    """Determine if the object instance is of a protected type.

    Objects of protected types are preserved as-is when passed to
    force_str(strings_only=True).
    """
    return isinstance(obj, _PROTECTED_TYPES)


def force_str(s, encoding="utf-8", strings_only=False, errors="strict"):
    """
    Similar to smart_str(), except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    # Handle the common case first for performance reasons.
    if issubclass(type(s), str):
        return s
    if strings_only and is_protected_type(s):
        return s
    try:
        if isinstance(s, bytes):
            s = str(s, encoding, errors)
        else:
            s = str(s)
    except UnicodeDecodeError as e:
        raise CustomUnicodeDecodeError(s, *e.args)
    return s


def bytes_to_dict(byte_data: bytes, charset: str = 'utf-8') -> Optional[Dict[str, Any]]:
    """
    Converts byte data to a dictionary. Assumes the byte data is JSON-encoded.

    Args:
        byte_data (bytes): The byte data to be converted to a dictionary.
        charset (str): The character encoding to use when decoding the byte data. Defaults to 'utf-8'.

    Returns:
        Optional[Dict[str, Any]]: The decoded dictionary if successful, or None if an error occurred.
    """
    try:
        # Decode the byte data into a JSON string using the specified charset
        json_string = byte_data.decode(charset)

        # Parse the JSON string into a Python dictionary
        return json.loads(json_string)
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        # Print an error message if decoding or parsing fails
        print(f"Error decoding bytes: {e}")

        # Return None to indicate that the conversion failed
        return None


def decompress_gzip(byte_data: bytes) -> bytes:
    """
    Decompresses gzip-compressed byte data.

    Args:
        byte_data (bytes): The gzip-compressed byte data to be decompressed.

    Returns:
        bytes: The decompressed byte data.
    """
    # Create an in-memory binary stream from the gzip-compressed byte data
    with io.BytesIO(byte_data) as byte_stream:
        # Open the gzip-compressed byte data as a GzipFile object
        with gzip.GzipFile(fileobj=byte_stream) as gz:
            # Read and return the decompressed byte data
            return gz.read()
