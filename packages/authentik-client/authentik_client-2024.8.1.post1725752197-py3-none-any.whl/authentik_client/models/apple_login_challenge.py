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

from pydantic import BaseModel, ConfigDict, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from authentik_client.models.contextual_flow_info import ContextualFlowInfo
from authentik_client.models.error_detail import ErrorDetail
from typing import Optional, Set
from typing_extensions import Self

class AppleLoginChallenge(BaseModel):
    """
    Special challenge for apple-native authentication flow, which happens on the client.
    """ # noqa: E501
    flow_info: Optional[ContextualFlowInfo] = None
    component: Optional[StrictStr] = 'ak-source-oauth-apple'
    response_errors: Optional[Dict[str, List[ErrorDetail]]] = None
    client_id: StrictStr
    scope: StrictStr
    redirect_uri: StrictStr
    state: StrictStr
    __properties: ClassVar[List[str]] = ["flow_info", "component", "response_errors", "client_id", "scope", "redirect_uri", "state"]

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
        """Create an instance of AppleLoginChallenge from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of flow_info
        if self.flow_info:
            _dict['flow_info'] = self.flow_info.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each value in response_errors (dict of array)
        _field_dict_of_array = {}
        if self.response_errors:
            for _key in self.response_errors:
                if self.response_errors[_key] is not None:
                    _field_dict_of_array[_key] = [
                        _item.to_dict() for _item in self.response_errors[_key]
                    ]
            _dict['response_errors'] = _field_dict_of_array
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AppleLoginChallenge from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "flow_info": ContextualFlowInfo.from_dict(obj["flow_info"]) if obj.get("flow_info") is not None else None,
            "component": obj.get("component") if obj.get("component") is not None else 'ak-source-oauth-apple',
            "response_errors": dict(
                (_k,
                        [ErrorDetail.from_dict(_item) for _item in _v]
                        if _v is not None
                        else None
                )
                for _k, _v in obj.get("response_errors", {}).items()
            ),
            "client_id": obj.get("client_id"),
            "scope": obj.get("scope"),
            "redirect_uri": obj.get("redirect_uri"),
            "state": obj.get("state")
        })
        return _obj


