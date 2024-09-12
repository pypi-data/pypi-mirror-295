# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Required, TypeAlias, TypedDict

from .flexible_chunks_param import FlexibleChunksParam
from .flexible_messages_param import FlexibleMessagesParam
from ..shared_params.chunk_extra_info_schema import ChunkExtraInfoSchema
from ..shared_params.string_extra_info_schema import StringExtraInfoSchema

__all__ = ["FlexibleTestCaseSchemaParam", "ExpectedExtraInfo"]

ExpectedExtraInfo: TypeAlias = Union[ChunkExtraInfoSchema, StringExtraInfoSchema]


class FlexibleTestCaseSchemaParam(TypedDict, total=False):
    input: Required[
        Union[
            str,
            float,
            Iterable[FlexibleChunksParam],
            Iterable[FlexibleMessagesParam],
            Iterable[object],
            Dict[
                str,
                Union[
                    str, float, Iterable[FlexibleChunksParam], Iterable[FlexibleMessagesParam], Iterable[object], object
                ],
            ],
            object,
        ]
    ]

    expected_extra_info: ExpectedExtraInfo

    expected_output: Union[
        str,
        float,
        Iterable[FlexibleChunksParam],
        Iterable[FlexibleMessagesParam],
        Iterable[object],
        Dict[
            str,
            Union[str, float, Iterable[FlexibleChunksParam], Iterable[FlexibleMessagesParam], Iterable[object], object],
        ],
        object,
    ]
