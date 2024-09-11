# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..shield_definition_param import ShieldDefinitionParam
from ..shared_params.attachment import Attachment
from ..shared_params.user_message import UserMessage
from ..tool_param_definition_param import ToolParamDefinitionParam
from ..shared_params.sampling_params import SamplingParams
from ..rest_api_execution_config_param import RestAPIExecutionConfigParam
from ..shared_params.tool_response_message import ToolResponseMessage

__all__ = [
    "TurnCreateParams",
    "Request",
    "RequestMessage",
    "RequestTool",
    "RequestToolBraveSearchToolDefinition",
    "RequestToolWolframAlphaToolDefinition",
    "RequestToolPhotogenToolDefinition",
    "RequestToolCodeInterpreterToolDefinition",
    "RequestToolFunctionCallToolDefinition",
    "RequestToolUnionMember5",
    "RequestToolUnionMember5MemoryBankConfig",
    "RequestToolUnionMember5MemoryBankConfigUnionMember0",
    "RequestToolUnionMember5MemoryBankConfigUnionMember1",
    "RequestToolUnionMember5MemoryBankConfigUnionMember2",
    "RequestToolUnionMember5MemoryBankConfigUnionMember3",
    "RequestToolUnionMember5QueryGeneratorConfig",
    "RequestToolUnionMember5QueryGeneratorConfigUnionMember0",
    "RequestToolUnionMember5QueryGeneratorConfigUnionMember1",
    "RequestToolUnionMember5QueryGeneratorConfigType",
]


class TurnCreateParams(TypedDict, total=False):
    request: Required[Request]


RequestMessage: TypeAlias = Union[UserMessage, ToolResponseMessage]


class RequestToolBraveSearchToolDefinition(TypedDict, total=False):
    type: Required[Literal["brave_search"]]

    input_shields: Iterable[ShieldDefinitionParam]

    output_shields: Iterable[ShieldDefinitionParam]

    remote_execution: RestAPIExecutionConfigParam


class RequestToolWolframAlphaToolDefinition(TypedDict, total=False):
    type: Required[Literal["wolfram_alpha"]]

    input_shields: Iterable[ShieldDefinitionParam]

    output_shields: Iterable[ShieldDefinitionParam]

    remote_execution: RestAPIExecutionConfigParam


class RequestToolPhotogenToolDefinition(TypedDict, total=False):
    type: Required[Literal["photogen"]]

    input_shields: Iterable[ShieldDefinitionParam]

    output_shields: Iterable[ShieldDefinitionParam]

    remote_execution: RestAPIExecutionConfigParam


class RequestToolCodeInterpreterToolDefinition(TypedDict, total=False):
    enable_inline_code_execution: Required[bool]

    type: Required[Literal["code_interpreter"]]

    input_shields: Iterable[ShieldDefinitionParam]

    output_shields: Iterable[ShieldDefinitionParam]

    remote_execution: RestAPIExecutionConfigParam


class RequestToolFunctionCallToolDefinition(TypedDict, total=False):
    description: Required[str]

    function_name: Required[str]

    parameters: Required[Dict[str, ToolParamDefinitionParam]]

    type: Required[Literal["function_call"]]

    input_shields: Iterable[ShieldDefinitionParam]

    output_shields: Iterable[ShieldDefinitionParam]

    remote_execution: RestAPIExecutionConfigParam


class RequestToolUnionMember5MemoryBankConfigUnionMember0(TypedDict, total=False):
    bank_id: Required[str]

    type: Required[Literal["vector"]]


class RequestToolUnionMember5MemoryBankConfigUnionMember1(TypedDict, total=False):
    bank_id: Required[str]

    keys: Required[List[str]]

    type: Required[Literal["keyvalue"]]


class RequestToolUnionMember5MemoryBankConfigUnionMember2(TypedDict, total=False):
    bank_id: Required[str]

    type: Required[Literal["keyword"]]


class RequestToolUnionMember5MemoryBankConfigUnionMember3(TypedDict, total=False):
    bank_id: Required[str]

    entities: Required[List[str]]

    type: Required[Literal["graph"]]


RequestToolUnionMember5MemoryBankConfig: TypeAlias = Union[
    RequestToolUnionMember5MemoryBankConfigUnionMember0,
    RequestToolUnionMember5MemoryBankConfigUnionMember1,
    RequestToolUnionMember5MemoryBankConfigUnionMember2,
    RequestToolUnionMember5MemoryBankConfigUnionMember3,
]


class RequestToolUnionMember5QueryGeneratorConfigUnionMember0(TypedDict, total=False):
    sep: Required[str]

    type: Required[Literal["default"]]


class RequestToolUnionMember5QueryGeneratorConfigUnionMember1(TypedDict, total=False):
    model: Required[str]

    template: Required[str]

    type: Required[Literal["llm"]]


class RequestToolUnionMember5QueryGeneratorConfigType(TypedDict, total=False):
    type: Required[Literal["custom"]]


RequestToolUnionMember5QueryGeneratorConfig: TypeAlias = Union[
    RequestToolUnionMember5QueryGeneratorConfigUnionMember0,
    RequestToolUnionMember5QueryGeneratorConfigUnionMember1,
    RequestToolUnionMember5QueryGeneratorConfigType,
]


class RequestToolUnionMember5(TypedDict, total=False):
    max_chunks: Required[int]

    max_tokens_in_context: Required[int]

    memory_bank_configs: Required[Iterable[RequestToolUnionMember5MemoryBankConfig]]

    query_generator_config: Required[RequestToolUnionMember5QueryGeneratorConfig]

    type: Required[Literal["memory"]]

    input_shields: Iterable[ShieldDefinitionParam]

    output_shields: Iterable[ShieldDefinitionParam]


RequestTool: TypeAlias = Union[
    RequestToolBraveSearchToolDefinition,
    RequestToolWolframAlphaToolDefinition,
    RequestToolPhotogenToolDefinition,
    RequestToolCodeInterpreterToolDefinition,
    RequestToolFunctionCallToolDefinition,
    RequestToolUnionMember5,
]


class Request(TypedDict, total=False):
    agent_id: Required[str]

    messages: Required[Iterable[RequestMessage]]

    session_id: Required[str]

    attachments: Iterable[Attachment]

    input_shields: Iterable[ShieldDefinitionParam]

    instructions: str

    output_shields: Iterable[ShieldDefinitionParam]

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
