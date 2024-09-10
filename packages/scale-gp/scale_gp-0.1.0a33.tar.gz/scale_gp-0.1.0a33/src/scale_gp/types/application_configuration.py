# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .application_edge import ApplicationEdge
from .application_node import ApplicationNode

__all__ = ["ApplicationConfiguration"]


class ApplicationConfiguration(BaseModel):
    edges: List[ApplicationEdge]

    nodes: List[ApplicationNode]
