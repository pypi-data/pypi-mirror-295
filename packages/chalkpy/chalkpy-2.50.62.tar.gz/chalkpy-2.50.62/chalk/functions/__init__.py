from typing import Any, Literal, Union

from chalk.features.underscore import (
    Underscore,
    UnderscoreBytesToString,
    UnderscoreCoalesce,
    UnderscoreGetJSONValue,
    UnderscoreGunzip,
    UnderscoreMD5,
    UnderscoreStringToBytes,
)


def string_to_bytes(expr: Any, encoding: Literal["utf-8", "hex", "base64"]):
    """
    Convert a string to bytes using the specified encoding.

    Parameters
    ----------
    expr
        A string feature to convert to bytes.
    encoding
        The encoding to use when converting the string to bytes.

    Examples
    --------
    >>> from chalk.functions import string_to_bytes
    >>> from chalk.features import _, features, Primary
    >>> @features
    ... class MyFeatures:
    ...    id: Primary[str]
    ...    name: str
    ...    hashed_name: bytes = string_to_bytes(_.name, encoding="utf-8")
    """
    return UnderscoreStringToBytes(expr, encoding)


def bytes_to_string(expr: Any, encoding: Literal["utf-8", "hex", "base64"]):
    """
    Convert bytes to a string using the specified encoding.

    Parameters
    ----------
    expr
        A bytes feature to convert to a string.
    encoding
        The encoding to use when converting the bytes to a string.

    Examples
    --------
    >>> from chalk.functions import bytes_to_string
    >>> from chalk.features import _, features, Primary
    >>> @features
    ... class MyFeatures:
    ...    id: Primary[str]
    ...    name: str
    ...    hashed_name: bytes
    ...    decoded_name: str = bytes_to_string(_.hashed_name, encoding="utf-8")
    """
    return UnderscoreBytesToString(expr, encoding)


def md5(expr: Any):
    """
    Compute the MD5 hash of some bytes.

    Parameters
    ----------
    expr
        A bytes feature to hash.

    Examples
    --------
    >>> from chalk.functions import md5
    >>> from chalk.features import _, features, Primary
    >>> @features
    ... class MyFeatures:
    ...    id: Primary[str]
    ...    bytes_feature: bytes
    ...    md5_bytes: bytes = md5(_.bytes_feature)
    """
    return UnderscoreMD5(expr)


def coalesce(*vals: Any):
    """
    Return the first non-null entry

    Parameters
    ----------
    vals
        Expressions to coalesce. They can be a combination of underscores and literals,
        though types must be compatible (ie do not coalesce int and string).

    Examples
    --------
    >>> from chalk.functions import coalesce
    >>> from chalk.features import _, features, Primary
    >>> from typing import Optional
    >>> @features
    ... class MyFeatures:
    ...    id: Primary[str]
    ...    a: Optional[int]
    ...    b: Optional[int]
    ...    c: int = coalesce(_.a, _.b, 7)
    """
    return UnderscoreCoalesce(*vals)


def json_value(expr: Underscore, path: Union[str, Underscore]):
    """
    Extract a scalar from a JSON feature using a JSONPath expression. The value of the referenced path must be a JSON
    scalar (boolean, number, string).

    Parameters
    ----------
    expr
        The JSON feature to query.
    path
        The JSONPath-like expression to extract the scalar from the JSON feature.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk import JSON
    >>> from chalk.features import _, features, Primary
    >>> @features
    ... class MyFeatures:
    ...    id: Primary[str]
    ...    raw: JSON
    ...    foo_value: str = F.json_value(_.raw, "$.foo.bar")
    """

    return UnderscoreGetJSONValue(expr, path)


def gunzip(expr: Underscore):
    """
    Decompress a GZIP-compressed bytes feature.

    Parameters
    ----------
    expr
        The GZIP-compressed bytes feature to decompress.

    Examples
    --------
    >>> import chalk.functions as F
    >>> from chalk.features import _, features, Primary
    >>> @features
    ... class MyFeatures:
    ...    id: Primary[str]
    ...    compressed_data: bytes
    ...    decompressed_data: bytes = F.gunzip(_.compressed_data)
    """
    return UnderscoreGunzip(expr)


__all__ = ("bytes_to_string", "coalesce", "gunzip", "md5", "json_value", "string_to_bytes")
