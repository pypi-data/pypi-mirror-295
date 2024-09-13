from datetime import datetime as _datetime

from django import template as _template
from django.conf import settings as _settings
from django.utils import dateparse as _dateparse

from b2_utils import helpers as _helpers

__all__ = [
    "get_settings",
    "cents_to_brl",
    "cnpj_parse",
    "cpf_parse",
    "index",
    "classname",
    "word",
    "get",
    "parse_datetime",
]

__register = _template.Library()


@__register.simple_tag(name="settings")
def get_settings(name):
    return getattr(_settings, name, "")


@__register.filter(name="brl")
def cents_to_brl(value: str | int):
    return _helpers.currency_parser(value)


@__register.filter(name="cnpj")
def cnpj_parse(value: str) -> str:
    return _helpers.cnpj_parser(value)


@__register.filter(name="cpf")
def cpf_parse(cpf_number: str) -> str:
    return _helpers.cpf_parser(cpf_number)


@__register.filter
def index(my_list, idx):
    try:
        return my_list[idx]
    except (IndexError, TypeError):
        return None


@__register.filter
def classname(obj):
    return obj.__class__.__name__


@__register.filter
def word(text: str, index: int):
    if text:
        return text.split()[index]

    return None


@__register.filter
def get(dictionary: dict | None, key: str):
    if isinstance(dictionary, dict):
        return dictionary.get(key)

    return dictionary


@__register.filter
def parse_datetime(date: str | None) -> _datetime:
    if not isinstance(date, str):
        return date

    return _dateparse.parse_datetime(date)
