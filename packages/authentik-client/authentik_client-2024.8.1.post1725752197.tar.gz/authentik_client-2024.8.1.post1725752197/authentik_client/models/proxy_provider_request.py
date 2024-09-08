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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from authentik_client.models.proxy_mode import ProxyMode
from typing import Optional, Set
from typing_extensions import Self

class ProxyProviderRequest(BaseModel):
    """
    ProxyProvider Serializer
    """ # noqa: E501
    name: Annotated[str, Field(min_length=1, strict=True)]
    authentication_flow: Optional[StrictStr] = Field(default=None, description="Flow used for authentication when the associated application is accessed by an un-authenticated user.")
    authorization_flow: StrictStr = Field(description="Flow used when authorizing this provider.")
    property_mappings: Optional[List[StrictStr]] = None
    internal_host: Optional[StrictStr] = None
    external_host: Annotated[str, Field(min_length=1, strict=True)]
    internal_host_ssl_validation: Optional[StrictBool] = Field(default=None, description="Validate SSL Certificates of upstream servers")
    certificate: Optional[StrictStr] = None
    skip_path_regex: Optional[StrictStr] = Field(default=None, description="Regular expressions for which authentication is not required. Each new line is interpreted as a new Regular Expression.")
    basic_auth_enabled: Optional[StrictBool] = Field(default=None, description="Set a custom HTTP-Basic Authentication header based on values from authentik.")
    basic_auth_password_attribute: Optional[StrictStr] = Field(default=None, description="User/Group Attribute used for the password part of the HTTP-Basic Header.")
    basic_auth_user_attribute: Optional[StrictStr] = Field(default=None, description="User/Group Attribute used for the user part of the HTTP-Basic Header. If not set, the user's Email address is used.")
    mode: Optional[ProxyMode] = Field(default=None, description="Enable support for forwardAuth in traefik and nginx auth_request. Exclusive with internal_host.")
    intercept_header_auth: Optional[StrictBool] = Field(default=None, description="When enabled, this provider will intercept the authorization header and authenticate requests based on its value.")
    cookie_domain: Optional[StrictStr] = None
    jwks_sources: Optional[List[StrictStr]] = None
    access_token_validity: Optional[Annotated[str, Field(min_length=1, strict=True)]] = Field(default=None, description="Tokens not valid on or after current time + this value (Format: hours=1;minutes=2;seconds=3).")
    refresh_token_validity: Optional[Annotated[str, Field(min_length=1, strict=True)]] = Field(default=None, description="Tokens not valid on or after current time + this value (Format: hours=1;minutes=2;seconds=3).")
    __properties: ClassVar[List[str]] = ["name", "authentication_flow", "authorization_flow", "property_mappings", "internal_host", "external_host", "internal_host_ssl_validation", "certificate", "skip_path_regex", "basic_auth_enabled", "basic_auth_password_attribute", "basic_auth_user_attribute", "mode", "intercept_header_auth", "cookie_domain", "jwks_sources", "access_token_validity", "refresh_token_validity"]

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
        """Create an instance of ProxyProviderRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # set to None if authentication_flow (nullable) is None
        # and model_fields_set contains the field
        if self.authentication_flow is None and "authentication_flow" in self.model_fields_set:
            _dict['authentication_flow'] = None

        # set to None if certificate (nullable) is None
        # and model_fields_set contains the field
        if self.certificate is None and "certificate" in self.model_fields_set:
            _dict['certificate'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ProxyProviderRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "authentication_flow": obj.get("authentication_flow"),
            "authorization_flow": obj.get("authorization_flow"),
            "property_mappings": obj.get("property_mappings"),
            "internal_host": obj.get("internal_host"),
            "external_host": obj.get("external_host"),
            "internal_host_ssl_validation": obj.get("internal_host_ssl_validation"),
            "certificate": obj.get("certificate"),
            "skip_path_regex": obj.get("skip_path_regex"),
            "basic_auth_enabled": obj.get("basic_auth_enabled"),
            "basic_auth_password_attribute": obj.get("basic_auth_password_attribute"),
            "basic_auth_user_attribute": obj.get("basic_auth_user_attribute"),
            "mode": obj.get("mode"),
            "intercept_header_auth": obj.get("intercept_header_auth"),
            "cookie_domain": obj.get("cookie_domain"),
            "jwks_sources": obj.get("jwks_sources"),
            "access_token_validity": obj.get("access_token_validity"),
            "refresh_token_validity": obj.get("refresh_token_validity")
        })
        return _obj


