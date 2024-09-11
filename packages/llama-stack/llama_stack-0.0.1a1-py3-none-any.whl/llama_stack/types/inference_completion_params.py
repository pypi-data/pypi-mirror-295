# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from typing_extensions import Required, TypedDict

from .shared_params.sampling_params import SamplingParams

__all__ = ["InferenceCompletionParams", "Request", "RequestLogprobs"]


class InferenceCompletionParams(TypedDict, total=False):
    request: Required[Request]


class RequestLogprobs(TypedDict, total=False):
    top_k: int


class Request(TypedDict, total=False):
    content: Required[Union[str, List[str]]]

    model: Required[str]

    logprobs: RequestLogprobs

    sampling_params: SamplingParams

    stream: bool
