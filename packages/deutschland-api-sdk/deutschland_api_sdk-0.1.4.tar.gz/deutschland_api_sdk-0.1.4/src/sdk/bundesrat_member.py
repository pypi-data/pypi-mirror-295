"""
bundesrat_member automatically generated by SDKgen please do not edit this file manually
https://sdkgen.app
"""

from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
import datetime
class BundesratMember(BaseModel):
    honorific_title: Optional[str] = Field(default=None, alias="honorificTitle")
    first_name: Optional[str] = Field(default=None, alias="firstName")
    name: Optional[str] = Field(default=None, alias="name")
    party: Optional[str] = Field(default=None, alias="party")
    state: Optional[str] = Field(default=None, alias="state")
    member: Optional[bool] = Field(default=None, alias="member")
    designated: Optional[bool] = Field(default=None, alias="designated")
    url: Optional[str] = Field(default=None, alias="url")
    image_path: Optional[str] = Field(default=None, alias="imagePath")
    image_date: Optional[datetime.datetime] = Field(default=None, alias="imageDate")
    detail: Optional[str] = Field(default=None, alias="detail")
    bio: Optional[str] = Field(default=None, alias="bio")
    address: Optional[str] = Field(default=None, alias="address")
    pass
