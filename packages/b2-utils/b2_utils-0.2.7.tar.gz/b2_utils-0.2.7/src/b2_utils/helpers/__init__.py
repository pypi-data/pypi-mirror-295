import base64 as _base64
import datetime as _datetime
import importlib as _importlib
import locale as _locale
import mimetypes as _mimetypes
import random as _random
import re as _re
import urllib.parse as _urlparse
from io import BytesIO as _BytesIO
from typing import Any as _Any
from urllib.parse import urlencode as _urlencode
from zoneinfo import ZoneInfo as _ZoneInfo

import requests as _requests
from django.conf import settings as _settings
from django.core.mail import get_connection as _get_connection
from django.core.mail import send_mail as _send_mail
from django.utils import timezone as _timezone

from b2_utils.helpers.auth import *  # noqa
from b2_utils.typing import Message as _Message
from b2_utils.typing import RangeHeader as _RangeHeader

__all__ = [
    "random_hex_color",
    "get_nested_attr",
    "update_url_querystring",
    "days_to_seconds",
    "cpf_parser",
    "cnpj_parser",
    "currency_parser",
    "get_component",
    "Alias",
    "hex_to_rgb",
    "luminance",
    "get_background_color",
    "send_mass_mail",
    "bytes_to_data_url",
    "pascal_to_snake",
    "string_to_date_obj",
    "load_from_url",
    "get_range_header",
    "write_in_buffer",
    "calculate_age",
]


def days_to_seconds(days):
    return days * 24 * 60 * 60


def random_hex_color(min_color=0x000000, max_color=0xFFFFFF) -> str:
    """Returns a random hexadecimal color in range [min_color, max_color], including
    both end points.

    Parameters
    ---------
    min_color : int
        Minimum value for color (default 0x000000)
    max_color : int
        Maximum value for color (default 0xFFFFFF)

    Returns
    -------
    str
        A random color "#XXXXXX" that is between min_color and max_color values.
    """

    return "#%06x".upper() % _random.randint(min_color, max_color)  # noqa: S311


def get_nested_attr(obj: any, path: str, raise_exception=False, default=None):
    """Gets nested object attributes, raising exceptions only when specified.

    Parameters
    ---------
    obj : any
        The object which attributes will be obtained
    path : str
        Attribute path separated with dots ('.') as usual
    raise_exception : bool = False
        If this value sets to True, an exception will be raised if an attribute cannot
        be obtained, even if default value is specified
    default : any = None
        A default value that's returned if the attribute can't be obtained. This
        parameter is ignored if raise_exception=True

    Returns
    -------
    any
        Attribute value or default value specified if any error occours while trying
        to get object attribute
    """

    for path_attr in path.split("."):
        if raise_exception:
            obj = getattr(obj, path_attr)
        else:
            obj = getattr(obj, path_attr, default)

    return obj


def update_url_querystring(
    url: str,
    params: dict,
    aditional_params: list[str] | None = None,
) -> str:
    """Updates the queryparams given a URL.

    Parameters
    ---------
    url: str
        The url you want to update.
    params: dict
        A dict with the new queryparams values.

    Returns
    -------
    str
        The full url, with updated queryparams.
    """
    url_parts = list(_urlparse.urlparse(url))
    query = dict(_urlparse.parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = _urlencode(query)
    if aditional_params:
        params = "&".join(aditional_params)
        if url_parts[4]:
            url_parts[4] += f"&{params}"

        else:
            url_parts[4] = params

    return _urlparse.urlunparse(url_parts)


def cpf_parser(value: str) -> str:
    return f"{value[:3]}.{value[3:6]}.{value[6:9]}-{value[9:12]}"


def cnpj_parser(value: str) -> str:
    return f"{value[:2]}.{value[2:5]}.{value[5:8]}/{value[8:12]}-{value[12:]}"


def currency_parser(value: str | int, encoding: str = "pt_BR.UTF-8") -> str:
    _locale.setlocale(_locale.LC_ALL, encoding)

    return _locale.currency(int(value) / 100, grouping=True)


def get_component(
    path: str,
    raise_exception: bool = True,
    default: _Any | None = None,
) -> _Any:
    """Retrieve a component from a specified Python module by its dotted path.

    This function imports a Python module and retrieves a component within it using the provided path. The path
    should be in the form 'module_name.component_name'. If the component is not found, and 'raise_exception' is
    set to True, a `AttributeError` will be raised. If 'raise_exception' is set to False, the 'default' value
    will be returned if the component is not found.

    Args:
        path (str): The dotted path to the desired component, e.g., 'module_name.component_name'.
        raise_exception (bool, optional): Whether to raise an exception if the component is not found.
            Defaults to True.
        default (any, optional): The default value to return if the component is not found when 'raise_exception'
            is set to False. Defaults to None.

    Returns:
        any: The requested component if found, or the default value if 'raise_exception' is set to False.

    Raises:
        AttributeError: If 'raise_exception' is True and the component is not found.

    Example:
        get_component("my_module.my_function")  # Returns the 'my_function' from 'my_module'.

    """
    module_name, component_name = path.rsplit(".", 1)
    module = _importlib.import_module(module_name)
    if raise_exception:
        return getattr(module, component_name)

    return getattr(module, component_name, default)


class Alias:
    def __init__(self, source_name, transform=None):
        self.source_name = source_name
        self.transform = transform

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        value = getattr(obj, self.source_name)

        if self.transform:
            value = self.transform(value)

        return value

    def __set__(self, obj, value):
        if self.transform:
            value = self.transform(value)

        setattr(obj, self.source_name, value)


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert a hexadecimal color to RGB."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def luminance(r: int, g: int, b: int) -> float:
    """Calculate the luminance of a color."""
    a = [r, g, b]
    for i in range(3):
        a[i] = a[i] / 255.0
        if a[i] <= 0.03928:  # noqa: PLR2004
            a[i] = a[i] / 12.92
        else:
            a[i] = ((a[i] + 0.055) / 1.055) ** 2.4
    return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722


def get_background_color(hex_color: str) -> str:
    """Returns the best text color for a given background color."""
    lum = luminance(*hex_to_rgb(hex_color))
    return "#000000" if lum > 0.179 else "#FFFFFF"  # noqa: PLR2004


def send_mass_mail(messages: list[_Message]):
    """Send multiple emails in a single connection, reducing the overhead of opening and closing the connection"""
    connection = _get_connection()
    connection.open()

    for subject, html_message, plain_message, email in messages:
        _send_mail(
            subject,
            plain_message,
            _settings.DEFAULT_FROM_EMAIL,
            [email],
            html_message=html_message,
            connection=connection,
        )

    connection.close()


def bytes_to_data_url(path: str, data: bytes) -> str:
    """Converts a file into a data URL.

    Parameters
    ---------
    path : str
        The file path
    data : bytes
        The file data

    Returns
    -------
    str
        The data URL

    check https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URLs
    """
    data = _base64.b64encode(data).decode("utf-8")
    type, _ = _mimetypes.guess_type(path)

    return f"data:{type};base64,{data}"


def pascal_to_snake(name):
    return _re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def string_to_date_obj(date: str, format: str):
    tz_info = _ZoneInfo(_settings.TIME_ZONE)
    date = date.replace("Z", "")

    return _datetime.datetime.strptime(date, format).astimezone(tz_info).date()


def load_from_url(url: str):
    """
    This function is used to load a file from a url and return a buffer.
    """
    buffer = _BytesIO()
    write_in_buffer(url, buffer)

    buffer.seek(0)

    return buffer


def get_range_header(
    buffer: _BytesIO,
    content_length: int,
) -> tuple[bool, _RangeHeader | None]:
    """
    This function is used to get the range header from a buffer.
    """
    buffer_size = buffer.__sizeof__()
    writer_all_content = buffer_size >= content_length

    if not writer_all_content:
        return writer_all_content, {"Range": f"bytes={buffer_size}-{content_length}"}

    return writer_all_content, None


def write_in_buffer(
    url: str,
    buffer: _BytesIO,
    headers: _RangeHeader | None = None,
    chunk_size: int = 1024 * 1024,
):
    """
    This function is used to write in a buffer from a url.
    """
    response = _requests.get(
        url,
        stream=True,
        headers=headers,
        timeout=10,
    )
    if response.ok:
        for chunk in response.iter_content(chunk_size):
            if chunk:
                buffer.write(chunk)

        is_complete, header = get_range_header(
            buffer,
            int(response.headers["Content-Length"]),
        )

        if not is_complete:
            write_in_buffer(url, buffer, header)

    return buffer


def calculate_age(date: _datetime.date) -> int:
    """This function is used to calculate the age of something based on the given date"""
    today = _timezone.now()
    return today.year - date.year - ((today.month, today.day) < (date.month, date.day))
