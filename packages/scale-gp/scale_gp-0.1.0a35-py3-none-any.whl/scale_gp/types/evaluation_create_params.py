# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .annotation_config_param import AnnotationConfigParam
from .multiturn_annotation_config_param import MultiturnAnnotationConfigParam
from .summarization_annotation_config_param import SummarizationAnnotationConfigParam

__all__ = [
    "EvaluationCreateParams",
    "EvaluationBuilderRequest",
    "EvaluationBuilderRequestAnnotationConfig",
    "DefaultEvaluationRequest",
    "DefaultEvaluationRequestAnnotationConfig",
]


class EvaluationBuilderRequest(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    application_spec_id: Required[str]

    application_variant_id: Required[str]

    description: Required[str]

    evaluation_dataset_id: Required[str]

    name: Required[str]

    annotation_config: EvaluationBuilderRequestAnnotationConfig
    """Annotation configuration for tasking"""

    evaluation_config: object

    evaluation_config_id: str
    """The ID of the associated evaluation config."""

    evaluation_dataset_version: int

    question_id_to_annotation_config: Dict[str, AnnotationConfigParam]
    """Specifies the annotation configuration to use for specific questions."""

    tags: object

    type: Literal["builder"]
    """
    create standalone evaluation or build evaluation which will auto generate test
    case results
    """


EvaluationBuilderRequestAnnotationConfig: TypeAlias = Union[
    AnnotationConfigParam, MultiturnAnnotationConfigParam, SummarizationAnnotationConfigParam
]


class DefaultEvaluationRequest(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    application_spec_id: Required[str]

    description: Required[str]

    name: Required[str]

    annotation_config: DefaultEvaluationRequestAnnotationConfig
    """Annotation configuration for tasking"""

    application_variant_id: str

    evaluation_config: object

    evaluation_config_id: str
    """The ID of the associated evaluation config."""

    question_id_to_annotation_config: Dict[str, AnnotationConfigParam]
    """Specifies the annotation configuration to use for specific questions."""

    tags: object

    type: Literal["default"]
    """
    create standalone evaluation or build evaluation which will auto generate test
    case results
    """


DefaultEvaluationRequestAnnotationConfig: TypeAlias = Union[
    AnnotationConfigParam, MultiturnAnnotationConfigParam, SummarizationAnnotationConfigParam
]

EvaluationCreateParams: TypeAlias = Union[EvaluationBuilderRequest, DefaultEvaluationRequest]
