# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .shared_params.user_message import UserMessage
from .tool_param_definition_param import ToolParamDefinitionParam
from .shared_params.system_message import SystemMessage
from .shared_params.sampling_params import SamplingParams
from .shared_params.completion_message import CompletionMessage
from .shared_params.tool_response_message import ToolResponseMessage

__all__ = ["InferenceChatCompletionParams", "Request", "RequestMessage", "RequestLogprobs", "RequestTool"]


class InferenceChatCompletionParams(TypedDict, total=False):
    request: Required[Request]


RequestMessage: TypeAlias = Union[UserMessage, SystemMessage, ToolResponseMessage, CompletionMessage]


class RequestLogprobs(TypedDict, total=False):
    top_k: int


class RequestTool(TypedDict, total=False):
    tool_name: Required[Union[Literal["brave_search", "wolfram_alpha", "photogen", "code_interpreter"], str]]

    description: str

    parameters: Dict[str, ToolParamDefinitionParam]


class Request(TypedDict, total=False):
    messages: Required[Iterable[RequestMessage]]

    model: Required[str]

    logprobs: RequestLogprobs

    sampling_params: SamplingParams

    stream: bool

    tool_choice: Literal["auto", "required"]

    tool_prompt_format: Literal["json", "function_tag"]
    """
    `json` -- Refers to the json format for calling tools. The json format takes the
    form like { "type": "function", "function" : { "name": "function_name",
    "description": "function_description", "parameters": {...} } }

    `function_tag` -- This is an example of how you could define your own user
    defined format for making tool calls. The function_tag format looks like this,
    <function=function_name>(parameters)</function>

    The detailed prompts for each of these formats are added to llama cli
    """

    tools: Iterable[RequestTool]
