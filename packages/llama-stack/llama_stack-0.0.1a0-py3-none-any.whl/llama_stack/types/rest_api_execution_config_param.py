# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, TypedDict

__all__ = ["RestAPIExecutionConfigParam"]


class RestAPIExecutionConfigParam(TypedDict, total=False):
    method: Required[Literal["GET", "POST", "PUT", "DELETE"]]

    url: Required[str]

    body: Dict[str, str]

    headers: Dict[str, str]

    params: Dict[str, str]
