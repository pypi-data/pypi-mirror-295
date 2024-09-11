from uuid import UUID
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    field_validator,
    ValidationError,
    field_serializer,
)
from .._utilities import Session
import httpx
from httpx import URL, Headers, Response
from typing import Optional
import logging
from .._exceptions import HopError
from .records import Record

logger = logging.getLogger(__name__)


class User(Record):
    user_name: str = Field(serialization_alias="userName")
