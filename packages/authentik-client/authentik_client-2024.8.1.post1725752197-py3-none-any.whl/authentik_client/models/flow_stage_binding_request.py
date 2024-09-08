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
from authentik_client.models.invalid_response_action_enum import InvalidResponseActionEnum
from authentik_client.models.policy_engine_mode import PolicyEngineMode
from typing import Optional, Set
from typing_extensions import Self

class FlowStageBindingRequest(BaseModel):
    """
    FlowStageBinding Serializer
    """ # noqa: E501
    target: StrictStr
    stage: StrictStr
    evaluate_on_plan: Optional[StrictBool] = Field(default=None, description="Evaluate policies during the Flow planning process.")
    re_evaluate_policies: Optional[StrictBool] = Field(default=None, description="Evaluate policies when the Stage is present to the user.")
    order: Annotated[int, Field(le=2147483647, strict=True, ge=-2147483648)]
    policy_engine_mode: Optional[PolicyEngineMode] = None
    invalid_response_action: Optional[InvalidResponseActionEnum] = Field(default=None, description="Configure how the flow executor should handle an invalid response to a challenge. RETRY returns the error message and a similar challenge to the executor. RESTART restarts the flow from the beginning, and RESTART_WITH_CONTEXT restarts the flow while keeping the current context.")
    __properties: ClassVar[List[str]] = ["target", "stage", "evaluate_on_plan", "re_evaluate_policies", "order", "policy_engine_mode", "invalid_response_action"]

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
        """Create an instance of FlowStageBindingRequest from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of FlowStageBindingRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "target": obj.get("target"),
            "stage": obj.get("stage"),
            "evaluate_on_plan": obj.get("evaluate_on_plan"),
            "re_evaluate_policies": obj.get("re_evaluate_policies"),
            "order": obj.get("order"),
            "policy_engine_mode": obj.get("policy_engine_mode"),
            "invalid_response_action": obj.get("invalid_response_action")
        })
        return _obj


