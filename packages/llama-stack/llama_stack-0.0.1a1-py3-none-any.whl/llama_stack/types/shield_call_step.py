# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ShieldCallStep", "Response"]


class Response(BaseModel):
    is_violation: bool

    shield_type: Union[
        Literal["llama_guard", "code_scanner_guard", "third_party_shield", "injection_shield", "jailbreak_shield"], str
    ]

    violation_return_message: Optional[str] = None

    violation_type: Optional[str] = None


class ShieldCallStep(BaseModel):
    response: Response

    step_id: str

    step_type: Literal["shield_call"]

    turn_id: str

    completed_at: Optional[datetime] = None

    started_at: Optional[datetime] = None
