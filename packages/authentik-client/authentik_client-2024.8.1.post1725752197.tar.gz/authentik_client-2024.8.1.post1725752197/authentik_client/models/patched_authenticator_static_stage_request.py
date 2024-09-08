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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from authentik_client.models.flow_set_request import FlowSetRequest
from typing import Optional, Set
from typing_extensions import Self

class PatchedAuthenticatorStaticStageRequest(BaseModel):
    """
    AuthenticatorStaticStage Serializer
    """ # noqa: E501
    name: Optional[Annotated[str, Field(min_length=1, strict=True)]] = None
    flow_set: Optional[List[FlowSetRequest]] = None
    configure_flow: Optional[StrictStr] = Field(default=None, description="Flow used by an authenticated user to configure this Stage. If empty, user will not be able to configure this stage.")
    friendly_name: Optional[Annotated[str, Field(min_length=1, strict=True)]] = None
    token_count: Optional[Annotated[int, Field(le=2147483647, strict=True, ge=0)]] = None
    token_length: Optional[Annotated[int, Field(le=2147483647, strict=True, ge=0)]] = None
    __properties: ClassVar[List[str]] = ["name", "flow_set", "configure_flow", "friendly_name", "token_count", "token_length"]

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
        """Create an instance of PatchedAuthenticatorStaticStageRequest from a JSON string"""
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

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PatchedAuthenticatorStaticStageRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "flow_set": [FlowSetRequest.from_dict(_item) for _item in obj["flow_set"]] if obj.get("flow_set") is not None else None,
            "configure_flow": obj.get("configure_flow"),
            "friendly_name": obj.get("friendly_name"),
            "token_count": obj.get("token_count"),
            "token_length": obj.get("token_length")
        })
        return _obj


