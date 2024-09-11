# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Required, TypeAlias, TypedDict

from .shared_params.user_message import UserMessage
from .shared_params.system_message import SystemMessage
from .shared_params.completion_message import CompletionMessage
from .shared_params.tool_response_message import ToolResponseMessage

__all__ = [
    "RewardScoringScoreParams",
    "Request",
    "RequestDialogGeneration",
    "RequestDialogGenerationDialog",
    "RequestDialogGenerationSampledGeneration",
]


class RewardScoringScoreParams(TypedDict, total=False):
    request: Required[Request]


RequestDialogGenerationDialog: TypeAlias = Union[UserMessage, SystemMessage, ToolResponseMessage, CompletionMessage]

RequestDialogGenerationSampledGeneration: TypeAlias = Union[
    UserMessage, SystemMessage, ToolResponseMessage, CompletionMessage
]


class RequestDialogGeneration(TypedDict, total=False):
    dialog: Required[Iterable[RequestDialogGenerationDialog]]

    sampled_generations: Required[Iterable[RequestDialogGenerationSampledGeneration]]


class Request(TypedDict, total=False):
    dialog_generations: Required[Iterable[RequestDialogGeneration]]

    model: Required[str]
