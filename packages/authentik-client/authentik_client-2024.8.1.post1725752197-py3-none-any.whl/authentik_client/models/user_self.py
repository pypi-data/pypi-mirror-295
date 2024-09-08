# coding: utf-8

"""
    authentik

    Making authentication simple.

    The version of the OpenAPI document: 2024.8.1
    Contact: hello@goauthentik.io
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from authentik_client.models.user_self_groups import UserSelfGroups
from authentik_client.models.user_type_enum import UserTypeEnum
from typing import Optional, Set
from typing_extensions import Self

class UserSelf(BaseModel):
    """
    User Serializer for information a user can retrieve about themselves
    """ # noqa: E501
    pk: StrictInt
    username: Annotated[str, Field(strict=True, max_length=150)] = Field(description="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.")
    name: StrictStr = Field(description="User's display name.")
    is_active: StrictBool = Field(description="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.")
    is_superuser: StrictBool
    groups: List[UserSelfGroups]
    email: Optional[Annotated[str, Field(strict=True, max_length=254)]] = None
    avatar: StrictStr = Field(description="User's avatar, either a http/https URL or a data URI")
    uid: StrictStr
    settings: Dict[str, Any] = Field(description="Get user settings with brand and group settings applied")
    type: Optional[UserTypeEnum] = None
    system_permissions: List[StrictStr] = Field(description="Get all system permissions assigned to the user")
    __properties: ClassVar[List[str]] = ["pk", "username", "name", "is_active", "is_superuser", "groups", "email", "avatar", "uid", "settings", "type", "system_permissions"]

    @field_validator('username')
    def username_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[\w.@+-]+$", value):
            raise ValueError(r"must validate the regular expression /^[\w.@+-]+$/")
        return value

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of UserSelf from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        """
        excluded_fields: Set[str] = set([
            "pk",
            "is_active",
            "is_superuser",
            "groups",
            "avatar",
            "uid",
            "settings",
            "system_permissions",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in groups (list)
        _items = []
        if self.groups:
            for _item in self.groups:
                if _item:
                    _items.append(_item.to_dict())
            _dict['groups'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of UserSelf from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "pk": obj.get("pk"),
            "username": obj.get("username"),
            "name": obj.get("name"),
            "is_active": obj.get("is_active"),
            "is_superuser": obj.get("is_superuser"),
            "groups": [UserSelfGroups.from_dict(_item) for _item in obj["groups"]] if obj.get("groups") is not None else None,
            "email": obj.get("email"),
            "avatar": obj.get("avatar"),
            "uid": obj.get("uid"),
            "settings": obj.get("settings"),
            "type": obj.get("type"),
            "system_permissions": obj.get("system_permissions")
        })
        return _obj


