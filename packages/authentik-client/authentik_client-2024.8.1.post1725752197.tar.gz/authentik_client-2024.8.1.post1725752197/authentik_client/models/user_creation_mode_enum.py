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
import json
from enum import Enum
from typing_extensions import Self


class UserCreationModeEnum(str, Enum):
    """
    UserCreationModeEnum
    """

    """
    allowed enum values
    """
    NEVER_CREATE = 'never_create'
    CREATE_WHEN_REQUIRED = 'create_when_required'
    ALWAYS_CREATE = 'always_create'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of UserCreationModeEnum from a JSON string"""
        return cls(json.loads(json_str))


