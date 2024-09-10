# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .multiturn_annotation_config_param import MultiturnAnnotationConfigParam
from .summarization_annotation_config_param import SummarizationAnnotationConfigParam

__all__ = [
    "EvaluationCreateParams",
    "EvaluationBuilderRequest",
    "EvaluationBuilderRequestAnnotationConfig",
    "EvaluationBuilderRequestAnnotationConfigAnnotationConfig",
    "EvaluationBuilderRequestAnnotationConfigAnnotationConfigComponent",
    "EvaluationBuilderRequestAnnotationConfigAnnotationConfigComponentItem",
    "EvaluationBuilderRequestAnnotationConfigAnnotationConfigComponentComparison",
    "EvaluationBuilderRequestQuestionIDToAnnotationConfig",
    "EvaluationBuilderRequestQuestionIDToAnnotationConfigComponent",
    "EvaluationBuilderRequestQuestionIDToAnnotationConfigComponentItem",
    "EvaluationBuilderRequestQuestionIDToAnnotationConfigComponentComparison",
    "DefaultEvaluationRequest",
    "DefaultEvaluationRequestAnnotationConfig",
    "DefaultEvaluationRequestAnnotationConfigAnnotationConfig",
    "DefaultEvaluationRequestAnnotationConfigAnnotationConfigComponent",
    "DefaultEvaluationRequestAnnotationConfigAnnotationConfigComponentItem",
    "DefaultEvaluationRequestAnnotationConfigAnnotationConfigComponentComparison",
    "DefaultEvaluationRequestQuestionIDToAnnotationConfig",
    "DefaultEvaluationRequestQuestionIDToAnnotationConfigComponent",
    "DefaultEvaluationRequestQuestionIDToAnnotationConfigComponentItem",
    "DefaultEvaluationRequestQuestionIDToAnnotationConfigComponentComparison",
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

    question_id_to_annotation_config: Dict[str, EvaluationBuilderRequestQuestionIDToAnnotationConfig]
    """Specifies the annotation configuration to use for specific questions."""

    tags: object

    type: Literal["builder"]
    """
    create standalone evaluation or build evaluation which will auto generate test
    case results
    """


class EvaluationBuilderRequestAnnotationConfigAnnotationConfigComponentItem(TypedDict, total=False):
    data_loc: Required[List[str]]

    label: str


class EvaluationBuilderRequestAnnotationConfigAnnotationConfigComponentComparison(TypedDict, total=False):
    data_loc: Required[List[str]]

    label: str


class EvaluationBuilderRequestAnnotationConfigAnnotationConfigComponent(TypedDict, total=False):
    item: Required[EvaluationBuilderRequestAnnotationConfigAnnotationConfigComponentItem]

    comparison: EvaluationBuilderRequestAnnotationConfigAnnotationConfigComponentComparison


class EvaluationBuilderRequestAnnotationConfigAnnotationConfig(TypedDict, total=False):
    components: Required[Iterable[EvaluationBuilderRequestAnnotationConfigAnnotationConfigComponent]]

    annotation_config_type: Literal["flexible", "summarization", "multiturn"]
    """An enumeration."""

    display: Literal["col", "row"]
    """An enumeration."""


EvaluationBuilderRequestAnnotationConfig: TypeAlias = Union[
    EvaluationBuilderRequestAnnotationConfigAnnotationConfig,
    MultiturnAnnotationConfigParam,
    SummarizationAnnotationConfigParam,
]


class EvaluationBuilderRequestQuestionIDToAnnotationConfigComponentItem(TypedDict, total=False):
    data_loc: Required[List[str]]

    label: str


class EvaluationBuilderRequestQuestionIDToAnnotationConfigComponentComparison(TypedDict, total=False):
    data_loc: Required[List[str]]

    label: str


class EvaluationBuilderRequestQuestionIDToAnnotationConfigComponent(TypedDict, total=False):
    item: Required[EvaluationBuilderRequestQuestionIDToAnnotationConfigComponentItem]

    comparison: EvaluationBuilderRequestQuestionIDToAnnotationConfigComponentComparison


class EvaluationBuilderRequestQuestionIDToAnnotationConfig(TypedDict, total=False):
    components: Required[Iterable[EvaluationBuilderRequestQuestionIDToAnnotationConfigComponent]]

    annotation_config_type: Literal["flexible", "summarization", "multiturn"]
    """An enumeration."""

    display: Literal["col", "row"]
    """An enumeration."""


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

    question_id_to_annotation_config: Dict[str, DefaultEvaluationRequestQuestionIDToAnnotationConfig]
    """Specifies the annotation configuration to use for specific questions."""

    tags: object

    type: Literal["default"]
    """
    create standalone evaluation or build evaluation which will auto generate test
    case results
    """


class DefaultEvaluationRequestAnnotationConfigAnnotationConfigComponentItem(TypedDict, total=False):
    data_loc: Required[List[str]]

    label: str


class DefaultEvaluationRequestAnnotationConfigAnnotationConfigComponentComparison(TypedDict, total=False):
    data_loc: Required[List[str]]

    label: str


class DefaultEvaluationRequestAnnotationConfigAnnotationConfigComponent(TypedDict, total=False):
    item: Required[DefaultEvaluationRequestAnnotationConfigAnnotationConfigComponentItem]

    comparison: DefaultEvaluationRequestAnnotationConfigAnnotationConfigComponentComparison


class DefaultEvaluationRequestAnnotationConfigAnnotationConfig(TypedDict, total=False):
    components: Required[Iterable[DefaultEvaluationRequestAnnotationConfigAnnotationConfigComponent]]

    annotation_config_type: Literal["flexible", "summarization", "multiturn"]
    """An enumeration."""

    display: Literal["col", "row"]
    """An enumeration."""


DefaultEvaluationRequestAnnotationConfig: TypeAlias = Union[
    DefaultEvaluationRequestAnnotationConfigAnnotationConfig,
    MultiturnAnnotationConfigParam,
    SummarizationAnnotationConfigParam,
]


class DefaultEvaluationRequestQuestionIDToAnnotationConfigComponentItem(TypedDict, total=False):
    data_loc: Required[List[str]]

    label: str


class DefaultEvaluationRequestQuestionIDToAnnotationConfigComponentComparison(TypedDict, total=False):
    data_loc: Required[List[str]]

    label: str


class DefaultEvaluationRequestQuestionIDToAnnotationConfigComponent(TypedDict, total=False):
    item: Required[DefaultEvaluationRequestQuestionIDToAnnotationConfigComponentItem]

    comparison: DefaultEvaluationRequestQuestionIDToAnnotationConfigComponentComparison


class DefaultEvaluationRequestQuestionIDToAnnotationConfig(TypedDict, total=False):
    components: Required[Iterable[DefaultEvaluationRequestQuestionIDToAnnotationConfigComponent]]

    annotation_config_type: Literal["flexible", "summarization", "multiturn"]
    """An enumeration."""

    display: Literal["col", "row"]
    """An enumeration."""


EvaluationCreateParams: TypeAlias = Union[EvaluationBuilderRequest, DefaultEvaluationRequest]
