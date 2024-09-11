# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .turn import Turn
from ..._models import BaseModel
from ..inference_step import InferenceStep
from ..shared.tool_call import ToolCall
from ..shield_call_step import ShieldCallStep
from ..tool_execution_step import ToolExecutionStep
from ..memory_retrieval_step import MemoryRetrievalStep

__all__ = [
    "AgenticSystemTurnStreamChunk",
    "Event",
    "EventPayload",
    "EventPayloadAgenticSystemTurnResponseStepStartPayload",
    "EventPayloadAgenticSystemTurnResponseStepProgressPayload",
    "EventPayloadAgenticSystemTurnResponseStepProgressPayloadToolCallDelta",
    "EventPayloadAgenticSystemTurnResponseStepProgressPayloadToolCallDeltaContent",
    "EventPayloadAgenticSystemTurnResponseStepCompletePayload",
    "EventPayloadAgenticSystemTurnResponseStepCompletePayloadStepDetails",
    "EventPayloadAgenticSystemTurnResponseTurnStartPayload",
    "EventPayloadAgenticSystemTurnResponseTurnCompletePayload",
]


class EventPayloadAgenticSystemTurnResponseStepStartPayload(BaseModel):
    event_type: Literal["step_start"]

    step_id: str

    step_type: Literal["inference", "tool_execution", "shield_call", "memory_retrieval"]

    metadata: Optional[Dict[str, Union[bool, float, str, List[object], object, None]]] = None


EventPayloadAgenticSystemTurnResponseStepProgressPayloadToolCallDeltaContent: TypeAlias = Union[str, ToolCall]


class EventPayloadAgenticSystemTurnResponseStepProgressPayloadToolCallDelta(BaseModel):
    content: EventPayloadAgenticSystemTurnResponseStepProgressPayloadToolCallDeltaContent

    parse_status: Literal["started", "in_progress", "failure", "success"]


class EventPayloadAgenticSystemTurnResponseStepProgressPayload(BaseModel):
    event_type: Literal["step_progress"]

    step_id: str

    step_type: Literal["inference", "tool_execution", "shield_call", "memory_retrieval"]

    text_delta_model_response: Optional[str] = FieldInfo(alias="model_response_text_delta", default=None)

    tool_call_delta: Optional[EventPayloadAgenticSystemTurnResponseStepProgressPayloadToolCallDelta] = None

    tool_response_text_delta: Optional[str] = None


EventPayloadAgenticSystemTurnResponseStepCompletePayloadStepDetails: TypeAlias = Union[
    InferenceStep, ToolExecutionStep, ShieldCallStep, MemoryRetrievalStep
]


class EventPayloadAgenticSystemTurnResponseStepCompletePayload(BaseModel):
    event_type: Literal["step_complete"]

    step_details: EventPayloadAgenticSystemTurnResponseStepCompletePayloadStepDetails

    step_type: Literal["inference", "tool_execution", "shield_call", "memory_retrieval"]


class EventPayloadAgenticSystemTurnResponseTurnStartPayload(BaseModel):
    event_type: Literal["turn_start"]

    turn_id: str


class EventPayloadAgenticSystemTurnResponseTurnCompletePayload(BaseModel):
    event_type: Literal["turn_complete"]

    turn: Turn


EventPayload: TypeAlias = Union[
    EventPayloadAgenticSystemTurnResponseStepStartPayload,
    EventPayloadAgenticSystemTurnResponseStepProgressPayload,
    EventPayloadAgenticSystemTurnResponseStepCompletePayload,
    EventPayloadAgenticSystemTurnResponseTurnStartPayload,
    EventPayloadAgenticSystemTurnResponseTurnCompletePayload,
]


class Event(BaseModel):
    payload: EventPayload


class AgenticSystemTurnStreamChunk(BaseModel):
    event: Event
