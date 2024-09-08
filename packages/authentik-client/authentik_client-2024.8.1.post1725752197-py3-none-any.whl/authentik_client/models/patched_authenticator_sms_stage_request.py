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
from authentik_client.models.auth_type_enum import AuthTypeEnum
from authentik_client.models.flow_set_request import FlowSetRequest
from authentik_client.models.provider_enum import ProviderEnum
from typing import Optional, Set
from typing_extensions import Self

class PatchedAuthenticatorSMSStageRequest(BaseModel):
    """
    AuthenticatorSMSStage Serializer
    """ # noqa: E501
    name: Optional[Annotated[str, Field(min_length=1, strict=True)]] = None
    flow_set: Optional[List[FlowSetRequest]] = None
    configure_flow: Optional[StrictStr] = Field(default=None, description="Flow used by an authenticated user to configure this Stage. If empty, user will not be able to configure this stage.")
    friendly_name: Optional[Annotated[str, Field(min_length=1, strict=True)]] = None
    provider: Optional[ProviderEnum] = None
    from_number: Optional[Annotated[str, Field(min_length=1, strict=True)]] = None
    account_sid: Optional[Annotated[str, Field(min_length=1, strict=True)]] = None
    auth: Optional[Annotated[str, Field(min_length=1, strict=True)]] = None
    auth_password: Optional[StrictStr] = None
    auth_type: Optional[AuthTypeEnum] = None
    verify_only: Optional[StrictBool] = Field(default=None, description="When enabled, the Phone number is only used during enrollment to verify the users authenticity. Only a hash of the phone number is saved to ensure it is not reused in the future.")
    mapping: Optional[StrictStr] = Field(default=None, description="Optionally modify the payload being sent to custom providers.")
    __properties: ClassVar[List[str]] = ["name", "flow_set", "configure_flow", "friendly_name", "provider", "from_number", "account_sid", "auth", "auth_password", "auth_type", "verify_only", "mapping"]

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
        """Create an instance of PatchedAuthenticatorSMSStageRequest from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in flow_set (list)
        _items = []
        if self.flow_set:
            for _item in self.flow_set:
                if _item:
                    _items.append(_item.to_dict())
            _dict['flow_set'] = _items
        # set to None if configure_flow (nullable) is None
        # and model_fields_set contains the field
        if self.configure_flow is None and "configure_flow" in self.model_fields_set:
            _dict['configure_flow'] = None

        # set to None if friendly_name (nullable) is None
        # and model_fields_set contains the field
        if self.friendly_name is None and "friendly_name" in self.model_fields_set:
            _dict['friendly_name'] = None

        # set to None if mapping (nullable) is None
        # and model_fields_set contains the field
        if self.mapping is None and "mapping" in self.model_fields_set:
            _dict['mapping'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PatchedAuthenticatorSMSStageRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "flow_set": [FlowSetRequest.from_dict(_item) for _item in obj["flow_set"]] if obj.get("flow_set") is not None else None,
            "configure_flow": obj.get("configure_flow"),
            "friendly_name": obj.get("friendly_name"),
            "provider": obj.get("provider"),
            "from_number": obj.get("from_number"),
            "account_sid": obj.get("account_sid"),
            "auth": obj.get("auth"),
            "auth_password": obj.get("auth_password"),
            "auth_type": obj.get("auth_type"),
            "verify_only": obj.get("verify_only"),
            "mapping": obj.get("mapping")
        })
        return _obj


