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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from authentik_client.models.policy_engine_mode import PolicyEngineMode
from authentik_client.models.user_matching_mode_enum import UserMatchingModeEnum
from typing import Optional, Set
from typing_extensions import Self

class PatchedLDAPSourceRequest(BaseModel):
    """
    LDAP Source Serializer
    """ # noqa: E501
    name: Optional[Annotated[str, Field(min_length=1, strict=True)]] = Field(default=None, description="Source's display Name.")
    slug: Optional[Annotated[str, Field(min_length=1, strict=True, max_length=50)]] = Field(default=None, description="Internal source name, used in URLs.")
    enabled: Optional[StrictBool] = None
    authentication_flow: Optional[StrictStr] = Field(default=None, description="Flow to use when authenticating existing users.")
    enrollment_flow: Optional[StrictStr] = Field(default=None, description="Flow to use when enrolling new users.")
    user_property_mappings: Optional[List[StrictStr]] = None
    group_property_mappings: Optional[List[StrictStr]] = None
    policy_engine_mode: Optional[PolicyEngineMode] = None
    user_matching_mode: Optional[UserMatchingModeEnum] = Field(default=None, description="How the source determines if an existing user should be authenticated or a new user enrolled.")
    user_path_template: Optional[Annotated[str, Field(min_length=1, strict=True)]] = None
    server_uri: Optional[Annotated[str, Field(min_length=1, strict=True)]] = None
    peer_certificate: Optional[StrictStr] = Field(default=None, description="Optionally verify the LDAP Server's Certificate against the CA Chain in this keypair.")
    client_certificate: Optional[StrictStr] = Field(default=None, description="Client certificate to authenticate against the LDAP Server's Certificate.")
    bind_cn: Optional[StrictStr] = None
    bind_password: Optional[StrictStr] = None
    start_tls: Optional[StrictBool] = None
    sni: Optional[StrictBool] = None
    base_dn: Optional[Annotated[str, Field(min_length=1, strict=True)]] = None
    additional_user_dn: Optional[StrictStr] = Field(default=None, description="Prepended to Base DN for User-queries.")
    additional_group_dn: Optional[StrictStr] = Field(default=None, description="Prepended to Base DN for Group-queries.")
    user_object_filter: Optional[Annotated[str, Field(min_length=1, strict=True)]] = Field(default=None, description="Consider Objects matching this filter to be Users.")
    group_object_filter: Optional[Annotated[str, Field(min_length=1, strict=True)]] = Field(default=None, description="Consider Objects matching this filter to be Groups.")
    group_membership_field: Optional[Annotated[str, Field(min_length=1, strict=True)]] = Field(default=None, description="Field which contains members of a group.")
    object_uniqueness_field: Optional[Annotated[str, Field(min_length=1, strict=True)]] = Field(default=None, description="Field which contains a unique Identifier.")
    password_login_update_internal_password: Optional[StrictBool] = Field(default=None, description="Update internal authentik password when login succeeds with LDAP")
    sync_users: Optional[StrictBool] = None
    sync_users_password: Optional[StrictBool] = Field(default=None, description="When a user changes their password, sync it back to LDAP. This can only be enabled on a single LDAP source.")
    sync_groups: Optional[StrictBool] = None
    sync_parent_group: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = ["name", "slug", "enabled", "authentication_flow", "enrollment_flow", "user_property_mappings", "group_property_mappings", "policy_engine_mode", "user_matching_mode", "user_path_template", "server_uri", "peer_certificate", "client_certificate", "bind_cn", "bind_password", "start_tls", "sni", "base_dn", "additional_user_dn", "additional_group_dn", "user_object_filter", "group_object_filter", "group_membership_field", "object_uniqueness_field", "password_login_update_internal_password", "sync_users", "sync_users_password", "sync_groups", "sync_parent_group"]

    @field_validator('slug')
    def slug_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r"^[-a-zA-Z0-9_]+$", value):
            raise ValueError(r"must validate the regular expression /^[-a-zA-Z0-9_]+$/")
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
        """Create an instance of PatchedLDAPSourceRequest from a JSON string"""
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

        # set to None if enrollment_flow (nullable) is None
        # and model_fields_set contains the field
        if self.enrollment_flow is None and "enrollment_flow" in self.model_fields_set:
            _dict['enrollment_flow'] = None

        # set to None if peer_certificate (nullable) is None
        # and model_fields_set contains the field
        if self.peer_certificate is None and "peer_certificate" in self.model_fields_set:
            _dict['peer_certificate'] = None

        # set to None if client_certificate (nullable) is None
        # and model_fields_set contains the field
        if self.client_certificate is None and "client_certificate" in self.model_fields_set:
            _dict['client_certificate'] = None

        # set to None if sync_parent_group (nullable) is None
        # and model_fields_set contains the field
        if self.sync_parent_group is None and "sync_parent_group" in self.model_fields_set:
            _dict['sync_parent_group'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PatchedLDAPSourceRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "slug": obj.get("slug"),
            "enabled": obj.get("enabled"),
            "authentication_flow": obj.get("authentication_flow"),
            "enrollment_flow": obj.get("enrollment_flow"),
            "user_property_mappings": obj.get("user_property_mappings"),
            "group_property_mappings": obj.get("group_property_mappings"),
            "policy_engine_mode": obj.get("policy_engine_mode"),
            "user_matching_mode": obj.get("user_matching_mode"),
            "user_path_template": obj.get("user_path_template"),
            "server_uri": obj.get("server_uri"),
            "peer_certificate": obj.get("peer_certificate"),
            "client_certificate": obj.get("client_certificate"),
            "bind_cn": obj.get("bind_cn"),
            "bind_password": obj.get("bind_password"),
            "start_tls": obj.get("start_tls"),
            "sni": obj.get("sni"),
            "base_dn": obj.get("base_dn"),
            "additional_user_dn": obj.get("additional_user_dn"),
            "additional_group_dn": obj.get("additional_group_dn"),
            "user_object_filter": obj.get("user_object_filter"),
            "group_object_filter": obj.get("group_object_filter"),
            "group_membership_field": obj.get("group_membership_field"),
            "object_uniqueness_field": obj.get("object_uniqueness_field"),
            "password_login_update_internal_password": obj.get("password_login_update_internal_password"),
            "sync_users": obj.get("sync_users"),
            "sync_users_password": obj.get("sync_users_password"),
            "sync_groups": obj.get("sync_groups"),
            "sync_parent_group": obj.get("sync_parent_group")
        })
        return _obj


