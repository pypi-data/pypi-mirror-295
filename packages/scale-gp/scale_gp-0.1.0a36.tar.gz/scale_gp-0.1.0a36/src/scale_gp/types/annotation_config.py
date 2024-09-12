# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["AnnotationConfig", "Component", "ComponentItem", "ComponentComparison"]


class ComponentItem(BaseModel):
    data_loc: List[str]

    label: Optional[str] = None


class ComponentComparison(BaseModel):
    data_loc: List[str]

    label: Optional[str] = None


class Component(BaseModel):
    item: ComponentItem

    comparison: Optional[ComponentComparison] = None


class AnnotationConfig(BaseModel):
    components: List[Component]

    annotation_config_type: Optional[Literal["flexible", "summarization", "multiturn"]] = None
    """An enumeration."""

    display: Optional[Literal["col", "row"]] = None
    """An enumeration."""
