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

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from authentik_client.models.authenticated_session_asn import AuthenticatedSessionAsn
from authentik_client.models.authenticated_session_geo_ip import AuthenticatedSessionGeoIp
from authentik_client.models.authenticated_session_user_agent import AuthenticatedSessionUserAgent
from typing import Optional, Set
from typing_extensions import Self

class AuthenticatedSession(BaseModel):
    """
    AuthenticatedSession Serializer
    """ # noqa: E501
    uuid: Optional[StrictStr] = None
    current: StrictBool = Field(description="Check if session is currently active session")
    user_agent: AuthenticatedSessionUserAgent
    geo_ip: Optional[AuthenticatedSessionGeoIp]
    asn: Optional[AuthenticatedSessionAsn]
    user: StrictInt
    last_ip: StrictStr
    last_user_agent: Optional[StrictStr] = None
    last_used: datetime
    expires: Optional[datetime] = None
    __properties: ClassVar[List[str]] = ["uuid", "current", "user_agent", "geo_ip", "asn", "user", "last_ip", "last_user_agent", "last_used", "expires"]

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
        """Create an instance of AuthenticatedSession from a JSON string"""
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
        """
        excluded_fields: Set[str] = set([
            "current",
            "last_used",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of user_agent
        if self.user_agent:
            _dict['user_agent'] = self.user_agent.to_dict()
        # override the default output from pydantic by calling `to_dict()` of geo_ip
        if self.geo_ip:
            _dict['geo_ip'] = self.geo_ip.to_dict()
        # override the default output from pydantic by calling `to_dict()` of asn
        if self.asn:
            _dict['asn'] = self.asn.to_dict()
        # set to None if geo_ip (nullable) is None
        # and model_fields_set contains the field
        if self.geo_ip is None and "geo_ip" in self.model_fields_set:
            _dict['geo_ip'] = None

        # set to None if asn (nullable) is None
        # and model_fields_set contains the field
        if self.asn is None and "asn" in self.model_fields_set:
            _dict['asn'] = None

        # set to None if expires (nullable) is None
        # and model_fields_set contains the field
        if self.expires is None and "expires" in self.model_fields_set:
            _dict['expires'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AuthenticatedSession from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "uuid": obj.get("uuid"),
            "current": obj.get("current"),
            "user_agent": AuthenticatedSessionUserAgent.from_dict(obj["user_agent"]) if obj.get("user_agent") is not None else None,
            "geo_ip": AuthenticatedSessionGeoIp.from_dict(obj["geo_ip"]) if obj.get("geo_ip") is not None else None,
            "asn": AuthenticatedSessionAsn.from_dict(obj["asn"]) if obj.get("asn") is not None else None,
            "user": obj.get("user"),
            "last_ip": obj.get("last_ip"),
            "last_user_agent": obj.get("last_user_agent"),
            "last_used": obj.get("last_used"),
            "expires": obj.get("expires")
        })
        return _obj


