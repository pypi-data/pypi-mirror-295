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


class SyncObjectModelEnum(str, Enum):
    """
    SyncObjectModelEnum
    """

    """
    allowed enum values
    """
    AUTHENTIK_DOT_CORE_DOT_MODELS_DOT_USER = 'authentik.core.models.User'
    AUTHENTIK_DOT_CORE_DOT_MODELS_DOT_GROUP = 'authentik.core.models.Group'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of SyncObjectModelEnum from a JSON string"""
        return cls(json.loads(json_str))


