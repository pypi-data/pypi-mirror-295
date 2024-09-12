# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from ..shared.chunk_extra_info_schema import ChunkExtraInfoSchema
from ..shared.result_schema_generation import ResultSchemaGeneration
from ..shared.string_extra_info_schema import StringExtraInfoSchema

__all__ = [
    "TestCaseResult",
    "GenerationTestCaseResultResponse",
    "FlexibleTestCaseResultResponse",
    "FlexibleTestCaseResultResponseTestCaseEvaluationData",
    "FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputArrayOfFlexibleIoChunk",
    "FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2",
    "FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk",
    "FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2",
    "FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationExtraInfo",
]


class GenerationTestCaseResultResponse(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_spec_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_user_id: str
    """The user who originally created the entity."""

    evaluation_dataset_id: str

    evaluation_dataset_version_num: str

    evaluation_id: str

    label_status: Literal["PENDING", "COMPLETED", "FAILED"]
    """An enumeration."""

    test_case_evaluation_data: ResultSchemaGeneration

    test_case_id: str

    annotated_by_user_id: Optional[str] = None
    """The user who annotated the task."""

    application_test_case_output_id: Optional[str] = None

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    audit_comment: Optional[str] = None

    audit_required: Optional[bool] = None

    audit_status: Optional[Literal["UNAUDITED", "FIXED", "APPROVED"]] = None
    """An enumeration."""

    completed_at: Optional[datetime] = None

    result: Optional[object] = None

    test_case_evaluation_data_schema: Optional[Literal["GENERATION"]] = None

    time_spent_labeling_s: Optional[int] = None
    """The time spent labeling in seconds."""


class FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputArrayOfFlexibleIoChunk(BaseModel):
    text: str

    metadata: Optional[object] = None


class FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk(
    BaseModel
):
    text: str

    metadata: Optional[object] = None


class FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]

FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationExtraInfo: TypeAlias = Annotated[
    Union[ChunkExtraInfoSchema, StringExtraInfoSchema], PropertyInfo(discriminator="schema_type")
]


class FlexibleTestCaseResultResponseTestCaseEvaluationData(BaseModel):
    generation_output: Union[
        str,
        float,
        List[FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputArrayOfFlexibleIoChunk],
        List[FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2],
        List[object],
        Dict[
            str,
            Union[
                str,
                float,
                List[
                    FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk
                ],
                List[
                    FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2
                ],
                List[object],
                object,
            ],
        ],
        object,
    ]

    generation_extra_info: Optional[FlexibleTestCaseResultResponseTestCaseEvaluationDataGenerationExtraInfo] = None


class FlexibleTestCaseResultResponse(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_spec_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_user_id: str
    """The user who originally created the entity."""

    evaluation_dataset_id: str

    evaluation_dataset_version_num: str

    evaluation_id: str

    label_status: Literal["PENDING", "COMPLETED", "FAILED"]
    """An enumeration."""

    test_case_evaluation_data: FlexibleTestCaseResultResponseTestCaseEvaluationData

    test_case_id: str

    annotated_by_user_id: Optional[str] = None
    """The user who annotated the task."""

    application_test_case_output_id: Optional[str] = None

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    audit_comment: Optional[str] = None

    audit_required: Optional[bool] = None

    audit_status: Optional[Literal["UNAUDITED", "FIXED", "APPROVED"]] = None
    """An enumeration."""

    completed_at: Optional[datetime] = None

    result: Optional[object] = None

    test_case_evaluation_data_schema: Optional[Literal["FLEXIBLE"]] = None

    time_spent_labeling_s: Optional[int] = None
    """The time spent labeling in seconds."""


TestCaseResult: TypeAlias = Annotated[
    Union[GenerationTestCaseResultResponse, FlexibleTestCaseResultResponse],
    PropertyInfo(discriminator="test_case_evaluation_data_schema"),
]
