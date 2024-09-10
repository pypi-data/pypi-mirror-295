# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .test_case_result import TestCaseResult
from ..evaluation_datasets.test_case import TestCase
from ..shared.chunk_extra_info_schema import ChunkExtraInfoSchema
from ..shared.result_schema_generation import ResultSchemaGeneration
from ..shared.string_extra_info_schema import StringExtraInfoSchema

__all__ = [
    "TestCaseResultWithViews",
    "GenerationTestCaseResultResponseWithViews",
    "GenerationTestCaseResultResponseWithViewsAnnotationResult",
    "GenerationTestCaseResultResponseWithViewsAnnotationResultLlmAutoEvalMetadata",
    "GenerationTestCaseResultResponseWithViewsTask",
    "GenerationTestCaseResultResponseWithViewsTaskAssignedTo",
    "FlexibleTestCaseResultResponseWithViews",
    "FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationData",
    "FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputArrayOfFlexibleIoChunk",
    "FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2",
    "FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk",
    "FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2",
    "FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationExtraInfo",
    "FlexibleTestCaseResultResponseWithViewsAnnotationResult",
    "FlexibleTestCaseResultResponseWithViewsAnnotationResultLlmAutoEvalMetadata",
    "FlexibleTestCaseResultResponseWithViewsTask",
    "FlexibleTestCaseResultResponseWithViewsTaskAssignedTo",
]


class GenerationTestCaseResultResponseWithViewsAnnotationResultLlmAutoEvalMetadata(BaseModel):
    annotation_result_id: str
    """The ID of the associated annotation result."""

    completion_tokens: int

    llm_reasoning: str
    """The reasoning the LLM gave for the annotation it provided."""

    prompt_tokens: int

    time_elapsed_s: int
    """The time elapsed to generate this annotation in seconds."""

    cost: Optional[int] = None
    """The cost of the annotation in cents."""


class GenerationTestCaseResultResponseWithViewsAnnotationResult(BaseModel):
    id: str
    """The unique identifier of the entity."""

    annotation_type: Literal["llm_auto", "human"]
    """An enumeration."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    question_id: str

    selected_choice: object
    """The selected choices(s) for the annotation result, in JSON form.

    For categorical questions, this is an object or list of objects (depending on if
    multiple selections are allowed). For free text questions, this is a string.
    """

    test_case_result_lineage_id: str

    llm_auto_eval_metadata: Optional[GenerationTestCaseResultResponseWithViewsAnnotationResultLlmAutoEvalMetadata] = (
        None
    )


class GenerationTestCaseResultResponseWithViewsTaskAssignedTo(BaseModel):
    id: str

    email: str

    first_name: Optional[str] = None

    last_name: Optional[str] = None


class GenerationTestCaseResultResponseWithViewsTask(BaseModel):
    id: str

    account_id: str
    """The ID of the account that owns the given entity."""

    priority: int

    status: Literal["PENDING", "COMPLETED"]
    """An enumeration."""

    task_entity_id: str

    task_entity_parent_id: str

    task_type: Literal["EVALUATION_ANNOTATION"]
    """An enumeration."""

    assigned_to: Optional[GenerationTestCaseResultResponseWithViewsTaskAssignedTo] = None

    assignment_expires_at: Optional[datetime] = None
    """The date and time when the task assignment expires in ISO format."""

    task_entity: Optional[TestCaseResult] = None
    """The entity that the task is associated with."""


class GenerationTestCaseResultResponseWithViews(BaseModel):
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

    annotation_results: Optional[List[GenerationTestCaseResultResponseWithViewsAnnotationResult]] = None

    application_test_case_output_id: Optional[str] = None

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    audit_comment: Optional[str] = None

    audit_required: Optional[bool] = None

    audit_status: Optional[Literal["UNAUDITED", "FIXED", "APPROVED"]] = None
    """An enumeration."""

    completed_at: Optional[datetime] = None

    metrics: Optional[Dict[str, float]] = None

    result: Optional[object] = None

    task: Optional[GenerationTestCaseResultResponseWithViewsTask] = None

    test_case_evaluation_data_schema: Optional[Literal["GENERATION"]] = None

    test_case_version: Optional[TestCase] = None

    time_spent_labeling_s: Optional[int] = None
    """The time spent labeling in seconds."""


class FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputArrayOfFlexibleIoChunk(BaseModel):
    text: str

    metadata: Optional[object] = None


class FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk(
    BaseModel
):
    text: str

    metadata: Optional[object] = None


class FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]

FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationExtraInfo: TypeAlias = Annotated[
    Union[ChunkExtraInfoSchema, StringExtraInfoSchema], PropertyInfo(discriminator="schema_type")
]


class FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationData(BaseModel):
    generation_output: Union[
        str,
        float,
        List[FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputArrayOfFlexibleIoChunk],
        List[FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2],
        List[object],
        Dict[
            str,
            Union[
                str,
                float,
                List[
                    FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk
                ],
                List[
                    FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesFlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2
                ],
                List[object],
                object,
            ],
        ],
        object,
    ]

    generation_extra_info: Optional[
        FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationDataGenerationExtraInfo
    ] = None


class FlexibleTestCaseResultResponseWithViewsAnnotationResultLlmAutoEvalMetadata(BaseModel):
    annotation_result_id: str
    """The ID of the associated annotation result."""

    completion_tokens: int

    llm_reasoning: str
    """The reasoning the LLM gave for the annotation it provided."""

    prompt_tokens: int

    time_elapsed_s: int
    """The time elapsed to generate this annotation in seconds."""

    cost: Optional[int] = None
    """The cost of the annotation in cents."""


class FlexibleTestCaseResultResponseWithViewsAnnotationResult(BaseModel):
    id: str
    """The unique identifier of the entity."""

    annotation_type: Literal["llm_auto", "human"]
    """An enumeration."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    question_id: str

    selected_choice: object
    """The selected choices(s) for the annotation result, in JSON form.

    For categorical questions, this is an object or list of objects (depending on if
    multiple selections are allowed). For free text questions, this is a string.
    """

    test_case_result_lineage_id: str

    llm_auto_eval_metadata: Optional[FlexibleTestCaseResultResponseWithViewsAnnotationResultLlmAutoEvalMetadata] = None


class FlexibleTestCaseResultResponseWithViewsTaskAssignedTo(BaseModel):
    id: str

    email: str

    first_name: Optional[str] = None

    last_name: Optional[str] = None


class FlexibleTestCaseResultResponseWithViewsTask(BaseModel):
    id: str

    account_id: str
    """The ID of the account that owns the given entity."""

    priority: int

    status: Literal["PENDING", "COMPLETED"]
    """An enumeration."""

    task_entity_id: str

    task_entity_parent_id: str

    task_type: Literal["EVALUATION_ANNOTATION"]
    """An enumeration."""

    assigned_to: Optional[FlexibleTestCaseResultResponseWithViewsTaskAssignedTo] = None

    assignment_expires_at: Optional[datetime] = None
    """The date and time when the task assignment expires in ISO format."""

    task_entity: Optional[TestCaseResult] = None
    """The entity that the task is associated with."""


class FlexibleTestCaseResultResponseWithViews(BaseModel):
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

    test_case_evaluation_data: FlexibleTestCaseResultResponseWithViewsTestCaseEvaluationData

    test_case_id: str

    annotated_by_user_id: Optional[str] = None
    """The user who annotated the task."""

    annotation_results: Optional[List[FlexibleTestCaseResultResponseWithViewsAnnotationResult]] = None

    application_test_case_output_id: Optional[str] = None

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    audit_comment: Optional[str] = None

    audit_required: Optional[bool] = None

    audit_status: Optional[Literal["UNAUDITED", "FIXED", "APPROVED"]] = None
    """An enumeration."""

    completed_at: Optional[datetime] = None

    metrics: Optional[Dict[str, float]] = None

    result: Optional[object] = None

    task: Optional[FlexibleTestCaseResultResponseWithViewsTask] = None

    test_case_evaluation_data_schema: Optional[Literal["FLEXIBLE"]] = None

    test_case_version: Optional[TestCase] = None

    time_spent_labeling_s: Optional[int] = None
    """The time spent labeling in seconds."""


TestCaseResultWithViews: TypeAlias = Annotated[
    Union[GenerationTestCaseResultResponseWithViews, FlexibleTestCaseResultResponseWithViews],
    PropertyInfo(discriminator="test_case_evaluation_data_schema"),
]
