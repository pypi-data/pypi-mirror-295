"""
bundestag_member automatically generated by SDKgen please do not edit this file manually
https://sdkgen.app
"""

from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
import datetime
from .bundestag_constituency import BundestagConstituency
class BundestagMember(BaseModel):
    id: Optional[str] = Field(default=None, alias="id")
    name: Optional[str] = Field(default=None, alias="name")
    party: Optional[str] = Field(default=None, alias="party")
    bio_url: Optional[str] = Field(default=None, alias="bioUrl")
    state: Optional[str] = Field(default=None, alias="state")
    constituency: Optional[BundestagConstituency] = Field(default=None, alias="constituency")
    elected: Optional[str] = Field(default=None, alias="elected")
    photo: Optional[str] = Field(default=None, alias="photo")
    photo_large: Optional[str] = Field(default=None, alias="photoLarge")
    photo_last_changed: Optional[datetime.datetime] = Field(default=None, alias="photoLastChanged")
    last_changed: Optional[datetime.datetime] = Field(default=None, alias="lastChanged")
    pass
