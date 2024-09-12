# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .shared.chunk_extra_info_schema import ChunkExtraInfoSchema
from .shared.result_schema_generation import ResultSchemaGeneration
from .shared.string_extra_info_schema import StringExtraInfoSchema
from .evaluation_datasets.flexible_chunk import FlexibleChunk
from .evaluation_datasets.flexible_message import FlexibleMessage

__all__ = [
    "ApplicationTestCaseOutput",
    "ApplicationTestCaseGenerationOutputResponse",
    "ApplicationTestCaseFlexibleOutputResponse",
    "ApplicationTestCaseFlexibleOutputResponseOutput",
    "ApplicationTestCaseFlexibleOutputResponseOutputGenerationExtraInfo",
]


class ApplicationTestCaseGenerationOutputResponse(BaseModel):
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

    metrics: Optional[Dict[str, float]] = None

    schema_type: Optional[Literal["GENERATION"]] = None


ApplicationTestCaseFlexibleOutputResponseOutputGenerationExtraInfo: TypeAlias = Annotated[
    Union[ChunkExtraInfoSchema, StringExtraInfoSchema], PropertyInfo(discriminator="schema_type")
]


class ApplicationTestCaseFlexibleOutputResponseOutput(BaseModel):
    generation_output: Union[
        str,
        float,
        List[FlexibleChunk],
        List[FlexibleMessage],
        List[object],
        Dict[str, Union[str, float, List[FlexibleChunk], List[FlexibleMessage], List[object], object]],
        object,
    ]

    generation_extra_info: Optional[ApplicationTestCaseFlexibleOutputResponseOutputGenerationExtraInfo] = None


class ApplicationTestCaseFlexibleOutputResponse(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    evaluation_dataset_id: str

    output: ApplicationTestCaseFlexibleOutputResponseOutput

    test_case_id: str

    application_interaction_id: Optional[str] = None

    metrics: Optional[Dict[str, float]] = None

    schema_type: Optional[Literal["FLEXIBLE"]] = None


ApplicationTestCaseOutput: TypeAlias = Annotated[
    Union[ApplicationTestCaseGenerationOutputResponse, ApplicationTestCaseFlexibleOutputResponse],
    PropertyInfo(discriminator="schema_type"),
]
