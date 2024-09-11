# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Required, TypeAlias, TypedDict

from .shield_definition_param import ShieldDefinitionParam
from .shared_params.user_message import UserMessage
from .shared_params.system_message import SystemMessage
from .shared_params.completion_message import CompletionMessage
from .shared_params.tool_response_message import ToolResponseMessage

__all__ = ["SafetyRunShieldsParams", "Request", "RequestMessage"]


class SafetyRunShieldsParams(TypedDict, total=False):
    request: Required[Request]


RequestMessage: TypeAlias = Union[UserMessage, SystemMessage, ToolResponseMessage, CompletionMessage]


class Request(TypedDict, total=False):
    messages: Required[Iterable[RequestMessage]]

    shields: Required[Iterable[ShieldDefinitionParam]]
