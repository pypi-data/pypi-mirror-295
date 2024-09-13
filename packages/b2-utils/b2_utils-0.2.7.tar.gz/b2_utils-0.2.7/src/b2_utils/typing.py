from typing import NamedTuple as _NamedTuple
from typing import TypedDict as _TypedDict

__all__ = ["RangeHeader", "Message"]


class Message(_NamedTuple):
    subject: str
    html_message: str
    plain_message: str
    email: str


class RangeHeader(_TypedDict):
    Range: str
