# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .evaluations import test_case_result
from .application_spec import ApplicationSpec
from .evaluation_dataset import EvaluationDataset
from .question_set_with_questions import QuestionSetWithQuestions
from .evaluation_datasets.test_case import TestCase
from .shared.chunk_extra_info_schema import ChunkExtraInfoSchema
from .shared.result_schema_generation import ResultSchemaGeneration
from .shared.string_extra_info_schema import StringExtraInfoSchema

__all__ = [
    "EvaluationWithViews",
    "AnnotationConfig",
    "AnnotationConfigComponent",
    "AnnotationConfigComponentItem",
    "AnnotationConfigComponentComparison",
    "AsyncJob",
    "EvaluationConfigExpanded",
    "EvaluationConfigExpandedEvaluationConfigExpanded",
    "EvaluationConfigExpandedLegacyEvaluationConfigExpanded",
    "EvaluationConfigExpandedLegacyEvaluationConfigExpandedQuestionSet",
    "EvaluationConfigExpandedLegacyEvaluationConfigExpandedQuestionSetQuestion",
    "QuestionIDToAnnotationConfig",
    "QuestionIDToAnnotationConfigComponent",
    "QuestionIDToAnnotationConfigComponentItem",
    "QuestionIDToAnnotationConfigComponentComparison",
    "TestCaseResult",
    "TestCaseResultGenerationTestCaseResultResponseExpanded",
    "TestCaseResultGenerationTestCaseResultResponseExpandedAnnotationResult",
    "TestCaseResultGenerationTestCaseResultResponseExpandedAnnotationResultLlmAutoEvalMetadata",
    "TestCaseResultGenerationTestCaseResultResponseExpandedTask",
    "TestCaseResultGenerationTestCaseResultResponseExpandedTaskAssignedTo",
    "TestCaseResultFlexibleTestCaseResultResponseExpanded",
    "TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationData",
    "TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputArrayOfFlexibleIoChunk",
    "TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2",
    "TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesTestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk",
    "TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesTestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2",
    "TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesTestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesTestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesTestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationExtraInfo",
    "TestCaseResultFlexibleTestCaseResultResponseExpandedAnnotationResult",
    "TestCaseResultFlexibleTestCaseResultResponseExpandedAnnotationResultLlmAutoEvalMetadata",
    "TestCaseResultFlexibleTestCaseResultResponseExpandedTask",
    "TestCaseResultFlexibleTestCaseResultResponseExpandedTaskAssignedTo",
]


class AnnotationConfigComponentItem(BaseModel):
    data_loc: List[str]

    label: Optional[str] = None


class AnnotationConfigComponentComparison(BaseModel):
    data_loc: List[str]

    label: Optional[str] = None


class AnnotationConfigComponent(BaseModel):
    item: AnnotationConfigComponentItem

    comparison: Optional[AnnotationConfigComponentComparison] = None


class AnnotationConfig(BaseModel):
    components: List[AnnotationConfigComponent]

    annotation_config_type: Optional[Literal["flexible", "summarization", "multiturn"]] = None
    """An enumeration."""

    display: Optional[Literal["col", "row"]] = None
    """An enumeration."""


class AsyncJob(BaseModel):
    id: str
    """The unique identifier of the entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    status: str

    updated_at: datetime
    """The date and time when the entity was last updated in ISO format."""

    job_metadata: Optional[object] = None

    job_type: Optional[str] = None

    parent_job_id: Optional[str] = None

    progress: Optional[object] = None


class EvaluationConfigExpandedEvaluationConfigExpanded(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_user_id: str
    """The user who originally created the entity."""

    evaluation_type: Literal["studio", "llm_auto", "human", "llm_benchmark"]
    """An enumeration."""

    question_set: QuestionSetWithQuestions

    question_set_id: str

    studio_project_id: Optional[str] = None


class EvaluationConfigExpandedLegacyEvaluationConfigExpandedQuestionSetQuestion(BaseModel):
    id: str
    """The unique identifier of the entity."""

    prompt: str

    title: str

    type: Literal["categorical", "free_text"]
    """An enumeration."""

    choices: Optional[List[object]] = None
    """List of choices for the question. Required for CATEGORICAL questions."""

    conditions: Optional[List[object]] = None
    """Conditions for the question to be shown."""

    multi: Optional[bool] = None
    """Whether the question allows multiple answers."""

    required: Optional[bool] = None
    """Whether the question is required."""


class EvaluationConfigExpandedLegacyEvaluationConfigExpandedQuestionSet(BaseModel):
    questions: List[EvaluationConfigExpandedLegacyEvaluationConfigExpandedQuestionSetQuestion]


class EvaluationConfigExpandedLegacyEvaluationConfigExpanded(BaseModel):
    evaluation_type: Literal["studio", "llm_auto", "human", "llm_benchmark"]
    """An enumeration."""

    question_set: EvaluationConfigExpandedLegacyEvaluationConfigExpandedQuestionSet

    studio_project_id: Optional[str] = None


EvaluationConfigExpanded: TypeAlias = Union[
    EvaluationConfigExpandedEvaluationConfigExpanded, EvaluationConfigExpandedLegacyEvaluationConfigExpanded
]


class QuestionIDToAnnotationConfigComponentItem(BaseModel):
    data_loc: List[str]

    label: Optional[str] = None


class QuestionIDToAnnotationConfigComponentComparison(BaseModel):
    data_loc: List[str]

    label: Optional[str] = None


class QuestionIDToAnnotationConfigComponent(BaseModel):
    item: QuestionIDToAnnotationConfigComponentItem

    comparison: Optional[QuestionIDToAnnotationConfigComponentComparison] = None


class QuestionIDToAnnotationConfig(BaseModel):
    components: List[QuestionIDToAnnotationConfigComponent]

    annotation_config_type: Optional[Literal["flexible", "summarization", "multiturn"]] = None
    """An enumeration."""

    display: Optional[Literal["col", "row"]] = None
    """An enumeration."""


class TestCaseResultGenerationTestCaseResultResponseExpandedAnnotationResultLlmAutoEvalMetadata(BaseModel):
    __test__ = False
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


class TestCaseResultGenerationTestCaseResultResponseExpandedAnnotationResult(BaseModel):
    __test__ = False
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

    llm_auto_eval_metadata: Optional[
        TestCaseResultGenerationTestCaseResultResponseExpandedAnnotationResultLlmAutoEvalMetadata
    ] = None


class TestCaseResultGenerationTestCaseResultResponseExpandedTaskAssignedTo(BaseModel):
    __test__ = False
    id: str

    email: str

    first_name: Optional[str] = None

    last_name: Optional[str] = None


class TestCaseResultGenerationTestCaseResultResponseExpandedTask(BaseModel):
    __test__ = False
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

    assigned_to: Optional[TestCaseResultGenerationTestCaseResultResponseExpandedTaskAssignedTo] = None

    assignment_expires_at: Optional[datetime] = None
    """The date and time when the task assignment expires in ISO format."""

    task_entity: Optional[test_case_result.TestCaseResult] = None
    """The entity that the task is associated with."""


class TestCaseResultGenerationTestCaseResultResponseExpanded(BaseModel):
    __test__ = False
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_spec_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_user_id: str
    """The user who originally created the entity."""

    evaluation_dataset: EvaluationDataset

    evaluation_dataset_id: str

    evaluation_dataset_version_num: str

    evaluation_id: str

    label_status: Literal["PENDING", "COMPLETED", "FAILED"]
    """An enumeration."""

    test_case_evaluation_data: ResultSchemaGeneration

    test_case_id: str

    test_case_version: TestCase

    annotated_by_user_id: Optional[str] = None
    """The user who annotated the task."""

    annotation_results: Optional[List[TestCaseResultGenerationTestCaseResultResponseExpandedAnnotationResult]] = None

    application_test_case_output_id: Optional[str] = None

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    audit_comment: Optional[str] = None

    audit_required: Optional[bool] = None

    audit_status: Optional[Literal["UNAUDITED", "FIXED", "APPROVED"]] = None
    """An enumeration."""

    completed_at: Optional[datetime] = None

    result: Optional[object] = None

    task: Optional[TestCaseResultGenerationTestCaseResultResponseExpandedTask] = None

    test_case_evaluation_data_schema: Optional[Literal["GENERATION"]] = None

    time_spent_labeling_s: Optional[int] = None
    """The time spent labeling in seconds."""


class TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputArrayOfFlexibleIoChunk(
    BaseModel
):
    __test__ = False
    text: str

    metadata: Optional[object] = None


class TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    __test__ = False
    content: str

    role: Optional[Literal["user"]] = None


class TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    __test__ = False
    content: str

    role: Optional[Literal["assistant"]] = None


class TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    __test__ = False
    content: str

    role: Optional[Literal["system"]] = None


TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesTestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk(
    BaseModel
):
    __test__ = False
    text: str

    metadata: Optional[object] = None


class TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesTestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    __test__ = False
    content: str

    role: Optional[Literal["user"]] = None


class TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesTestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    __test__ = False
    content: str

    role: Optional[Literal["assistant"]] = None


class TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesTestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    __test__ = False
    content: str

    role: Optional[Literal["system"]] = None


TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesTestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesTestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesTestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesTestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]

TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationExtraInfo: TypeAlias = Annotated[
    Union[ChunkExtraInfoSchema, StringExtraInfoSchema], PropertyInfo(discriminator="schema_type")
]


class TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationData(BaseModel):
    __test__ = False
    generation_output: Union[
        str,
        float,
        List[
            TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputArrayOfFlexibleIoChunk
        ],
        List[
            TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputArrayOfChatMessageV2
        ],
        List[object],
        Dict[
            str,
            Union[
                str,
                float,
                List[
                    TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesTestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk
                ],
                List[
                    TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesTestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2
                ],
                List[object],
                object,
            ],
        ],
        object,
    ]

    generation_extra_info: Optional[
        TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationDataGenerationExtraInfo
    ] = None


class TestCaseResultFlexibleTestCaseResultResponseExpandedAnnotationResultLlmAutoEvalMetadata(BaseModel):
    __test__ = False
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


class TestCaseResultFlexibleTestCaseResultResponseExpandedAnnotationResult(BaseModel):
    __test__ = False
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

    llm_auto_eval_metadata: Optional[
        TestCaseResultFlexibleTestCaseResultResponseExpandedAnnotationResultLlmAutoEvalMetadata
    ] = None


class TestCaseResultFlexibleTestCaseResultResponseExpandedTaskAssignedTo(BaseModel):
    __test__ = False
    id: str

    email: str

    first_name: Optional[str] = None

    last_name: Optional[str] = None


class TestCaseResultFlexibleTestCaseResultResponseExpandedTask(BaseModel):
    __test__ = False
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

    assigned_to: Optional[TestCaseResultFlexibleTestCaseResultResponseExpandedTaskAssignedTo] = None

    assignment_expires_at: Optional[datetime] = None
    """The date and time when the task assignment expires in ISO format."""

    task_entity: Optional[test_case_result.TestCaseResult] = None
    """The entity that the task is associated with."""


class TestCaseResultFlexibleTestCaseResultResponseExpanded(BaseModel):
    __test__ = False
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_spec_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_user_id: str
    """The user who originally created the entity."""

    evaluation_dataset: EvaluationDataset

    evaluation_dataset_id: str

    evaluation_dataset_version_num: str

    evaluation_id: str

    label_status: Literal["PENDING", "COMPLETED", "FAILED"]
    """An enumeration."""

    test_case_evaluation_data: TestCaseResultFlexibleTestCaseResultResponseExpandedTestCaseEvaluationData

    test_case_id: str

    test_case_version: TestCase

    annotated_by_user_id: Optional[str] = None
    """The user who annotated the task."""

    annotation_results: Optional[List[TestCaseResultFlexibleTestCaseResultResponseExpandedAnnotationResult]] = None

    application_test_case_output_id: Optional[str] = None

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    audit_comment: Optional[str] = None

    audit_required: Optional[bool] = None

    audit_status: Optional[Literal["UNAUDITED", "FIXED", "APPROVED"]] = None
    """An enumeration."""

    completed_at: Optional[datetime] = None

    result: Optional[object] = None

    task: Optional[TestCaseResultFlexibleTestCaseResultResponseExpandedTask] = None

    test_case_evaluation_data_schema: Optional[Literal["FLEXIBLE"]] = None

    time_spent_labeling_s: Optional[int] = None
    """The time spent labeling in seconds."""


TestCaseResult: TypeAlias = Annotated[
    Union[TestCaseResultGenerationTestCaseResultResponseExpanded, TestCaseResultFlexibleTestCaseResultResponseExpanded],
    PropertyInfo(discriminator="test_case_evaluation_data_schema"),
]


class EvaluationWithViews(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_spec_id: str

    completed_test_case_result_count: int
    """The number of test case results that have been completed for the evaluation"""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_user_id: str
    """The user who originally created the entity."""

    description: str

    name: str

    status: Literal["PENDING", "COMPLETED", "FAILED"]
    """An enumeration."""

    total_test_case_result_count: int
    """The total number of test case results for the evaluation"""

    annotation_config: Optional[AnnotationConfig] = None
    """Annotation configuration for tasking"""

    application_spec: Optional[ApplicationSpec] = None

    application_variant_id: Optional[str] = None

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    async_jobs: Optional[List[AsyncJob]] = None

    completed_at: Optional[datetime] = None
    """
    The date and time that all test case results for the evaluation were completed
    for the evaluation in ISO format.
    """

    evaluation_config: Optional[object] = None

    evaluation_config_expanded: Optional[EvaluationConfigExpanded] = None

    evaluation_config_id: Optional[str] = None
    """The ID of the associated evaluation config."""

    question_id_to_annotation_config: Optional[Dict[str, QuestionIDToAnnotationConfig]] = None
    """Specifies the annotation configuration to use for specific questions."""

    tags: Optional[object] = None

    test_case_results: Optional[List[TestCaseResult]] = None
