# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, TypedDict

from .train_eval_dataset_param import TrainEvalDatasetParam

__all__ = [
    "PostTrainingPreferenceOptimizeParams",
    "Request",
    "RequestAlgorithmConfig",
    "RequestOptimizerConfig",
    "RequestTrainingConfig",
]


class PostTrainingPreferenceOptimizeParams(TypedDict, total=False):
    request: Required[Request]


class RequestAlgorithmConfig(TypedDict, total=False):
    epsilon: Required[float]

    gamma: Required[float]

    reward_clip: Required[float]

    reward_scale: Required[float]


class RequestOptimizerConfig(TypedDict, total=False):
    lr: Required[float]

    lr_min: Required[float]

    optimizer_type: Required[Literal["adam", "adamw", "sgd"]]

    weight_decay: Required[float]


class RequestTrainingConfig(TypedDict, total=False):
    batch_size: Required[int]

    enable_activation_checkpointing: Required[bool]

    fsdp_cpu_offload: Required[bool]

    memory_efficient_fsdp_wrap: Required[bool]

    n_epochs: Required[int]

    n_iters: Required[int]

    shuffle: Required[bool]


class Request(TypedDict, total=False):
    algorithm: Required[Literal["dpo"]]

    algorithm_config: Required[RequestAlgorithmConfig]

    dataset: Required[TrainEvalDatasetParam]

    finetuned_model: Required[str]

    hyperparam_search_config: Required[Dict[str, Union[bool, float, str, Iterable[object], object, None]]]

    job_uuid: Required[str]

    logger_config: Required[Dict[str, Union[bool, float, str, Iterable[object], object, None]]]

    optimizer_config: Required[RequestOptimizerConfig]

    training_config: Required[RequestTrainingConfig]

    validation_dataset: Required[TrainEvalDatasetParam]
