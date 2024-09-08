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


class NetworkBindingEnum(str, Enum):
    """
    NetworkBindingEnum
    """

    """
    allowed enum values
    """
    NO_BINDING = 'no_binding'
    BIND_ASN = 'bind_asn'
    BIND_ASN_NETWORK = 'bind_asn_network'
    BIND_ASN_NETWORK_IP = 'bind_asn_network_ip'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of NetworkBindingEnum from a JSON string"""
        return cls(json.loads(json_str))


