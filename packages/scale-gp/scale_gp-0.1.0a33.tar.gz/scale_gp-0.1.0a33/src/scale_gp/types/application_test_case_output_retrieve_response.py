# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .evaluation_trace_span import EvaluationTraceSpan
from .application_metric_score import ApplicationMetricScore
from .evaluation_datasets.test_case import TestCase
from .shared.chunk_extra_info_schema import ChunkExtraInfoSchema
from .shared.result_schema_generation import ResultSchemaGeneration
from .shared.string_extra_info_schema import StringExtraInfoSchema

__all__ = [
    "ApplicationTestCaseOutputRetrieveResponse",
    "ApplicationTestCaseGenerationOutputResponseWithViews",
    "ApplicationTestCaseGenerationOutputResponseWithViewsInteraction",
    "ApplicationTestCaseFlexibleOutputResponseWithViews",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutput",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfFlexibleIoChunk",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationExtraInfo",
    "ApplicationTestCaseFlexibleOutputResponseWithViewsInteraction",
]


class ApplicationTestCaseGenerationOutputResponseWithViewsInteraction(BaseModel):
    id: str

    application_spec_id: str

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    duration_ms: int
    """How much time the step took in milliseconds(ms)"""

    input: object

    operation_status: Literal["SUCCESS", "ERROR"]
    """An enumeration."""

    output: object

    start_timestamp: datetime

    chat_thread_id: Optional[str] = None

    interaction_source: Optional[Literal["EXTERNAL_AI", "EVALUATION", "SGP_CHAT"]] = None
    """An enumeration."""

    operation_metadata: Optional[object] = None
    """The JSON representation of the metadata insights emitted through the execution.

    This can differ based on different types of operations
    """

    trace_spans: Optional[List[EvaluationTraceSpan]] = None


class ApplicationTestCaseGenerationOutputResponseWithViews(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    evaluation_dataset_id: str

    output: ResultSchemaGeneration

    test_case_id: str

    application_interaction_id: Optional[str] = None

    interaction: Optional[ApplicationTestCaseGenerationOutputResponseWithViewsInteraction] = None

    metric_scores: Optional[List[ApplicationMetricScore]] = None

    metrics: Optional[Dict[str, float]] = None

    schema_type: Optional[Literal["GENERATION"]] = None

    test_case_version: Optional[TestCase] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfFlexibleIoChunk(BaseModel):
    text: str

    metadata: Optional[object] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk(
    BaseModel
):
    text: str

    metadata: Optional[object] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]

ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationExtraInfo: TypeAlias = Annotated[
    Union[ChunkExtraInfoSchema, StringExtraInfoSchema], PropertyInfo(discriminator="schema_type")
]


class ApplicationTestCaseFlexibleOutputResponseWithViewsOutput(BaseModel):
    generation_output: Union[
        str,
        float,
        List[ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfFlexibleIoChunk],
        List[ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputArrayOfChatMessageV2],
        List[object],
        Dict[
            str,
            Union[
                str,
                float,
                List[
                    ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk
                ],
                List[
                    ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2
                ],
                List[object],
                object,
            ],
        ],
        object,
    ]

    generation_extra_info: Optional[ApplicationTestCaseFlexibleOutputResponseWithViewsOutputGenerationExtraInfo] = None


class ApplicationTestCaseFlexibleOutputResponseWithViewsInteraction(BaseModel):
    id: str

    application_spec_id: str

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    duration_ms: int
    """How much time the step took in milliseconds(ms)"""

    input: object

    operation_status: Literal["SUCCESS", "ERROR"]
    """An enumeration."""

    output: object

    start_timestamp: datetime

    chat_thread_id: Optional[str] = None

    interaction_source: Optional[Literal["EXTERNAL_AI", "EVALUATION", "SGP_CHAT"]] = None
    """An enumeration."""

    operation_metadata: Optional[object] = None
    """The JSON representation of the metadata insights emitted through the execution.

    This can differ based on different types of operations
    """

    trace_spans: Optional[List[EvaluationTraceSpan]] = None


class ApplicationTestCaseFlexibleOutputResponseWithViews(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    evaluation_dataset_id: str

    output: ApplicationTestCaseFlexibleOutputResponseWithViewsOutput

    test_case_id: str

    application_interaction_id: Optional[str] = None

    interaction: Optional[ApplicationTestCaseFlexibleOutputResponseWithViewsInteraction] = None

    metric_scores: Optional[List[ApplicationMetricScore]] = None

    metrics: Optional[Dict[str, float]] = None

    schema_type: Optional[Literal["FLEXIBLE"]] = None

    test_case_version: Optional[TestCase] = None


ApplicationTestCaseOutputRetrieveResponse: TypeAlias = Annotated[
    Union[ApplicationTestCaseGenerationOutputResponseWithViews, ApplicationTestCaseFlexibleOutputResponseWithViews],
    PropertyInfo(discriminator="schema_type"),
]
