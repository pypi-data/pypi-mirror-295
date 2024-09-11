# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .train_eval_dataset_param import TrainEvalDatasetParam

__all__ = [
    "PostTrainingSupervisedFineTuneParams",
    "Request",
    "RequestAlgorithmConfig",
    "RequestAlgorithmConfigLoraFinetuningConfig",
    "RequestAlgorithmConfigQLoraFinetuningConfig",
    "RequestAlgorithmConfigDoraFinetuningConfig",
    "RequestOptimizerConfig",
    "RequestTrainingConfig",
]


class PostTrainingSupervisedFineTuneParams(TypedDict, total=False):
    request: Required[Request]


class RequestAlgorithmConfigLoraFinetuningConfig(TypedDict, total=False):
    alpha: Required[int]

    apply_lora_to_mlp: Required[bool]

    apply_lora_to_output: Required[bool]

    lora_attn_modules: Required[List[str]]

    rank: Required[int]


class RequestAlgorithmConfigQLoraFinetuningConfig(TypedDict, total=False):
    alpha: Required[int]

    apply_lora_to_mlp: Required[bool]

    apply_lora_to_output: Required[bool]

    lora_attn_modules: Required[List[str]]

    rank: Required[int]


class RequestAlgorithmConfigDoraFinetuningConfig(TypedDict, total=False):
    alpha: Required[int]

    apply_lora_to_mlp: Required[bool]

    apply_lora_to_output: Required[bool]

    lora_attn_modules: Required[List[str]]

    rank: Required[int]


RequestAlgorithmConfig: TypeAlias = Union[
    RequestAlgorithmConfigLoraFinetuningConfig,
    RequestAlgorithmConfigQLoraFinetuningConfig,
    RequestAlgorithmConfigDoraFinetuningConfig,
]


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
    algorithm: Required[Literal["full", "lora", "qlora", "dora"]]

    algorithm_config: Required[RequestAlgorithmConfig]

    dataset: Required[TrainEvalDatasetParam]

    hyperparam_search_config: Required[Dict[str, Union[bool, float, str, Iterable[object], object, None]]]

    job_uuid: Required[str]

    logger_config: Required[Dict[str, Union[bool, float, str, Iterable[object], object, None]]]

    model: Required[str]

    optimizer_config: Required[RequestOptimizerConfig]

    training_config: Required[RequestTrainingConfig]

    validation_dataset: Required[TrainEvalDatasetParam]
