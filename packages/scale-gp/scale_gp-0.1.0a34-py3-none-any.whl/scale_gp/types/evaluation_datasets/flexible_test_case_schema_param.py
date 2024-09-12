# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..shared_params.chunk_extra_info_schema import ChunkExtraInfoSchema
from ..shared_params.string_extra_info_schema import StringExtraInfoSchema

__all__ = [
    "FlexibleTestCaseSchemaParam",
    "InputArrayOfFlexibleIoChunk",
    "InputArrayOfChatMessageV2",
    "InputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "InputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "InputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk",
    "InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfChatMessageV2",
    "InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ExpectedExtraInfo",
    "ExpectedOutputArrayOfFlexibleIoChunk",
    "ExpectedOutputArrayOfChatMessageV2",
    "ExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
    "ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk",
    "ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2",
    "ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage",
    "ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage",
    "ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage",
]


class InputArrayOfFlexibleIoChunk(TypedDict, total=False):
    text: Required[str]

    metadata: object


class InputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(TypedDict, total=False):
    content: Required[str]

    role: Literal["user"]


class InputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(TypedDict, total=False):
    content: Required[str]

    role: Literal["assistant"]


class InputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(TypedDict, total=False):
    content: Required[str]

    role: Literal["system"]


InputArrayOfChatMessageV2: TypeAlias = Union[
    InputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
    InputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
    InputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
]


class InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk(TypedDict, total=False):
    text: Required[str]

    metadata: object


class InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["user"]


class InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["assistant"]


class InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["system"]


InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfChatMessageV2: TypeAlias = Union[
    InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
    InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
    InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
]

ExpectedExtraInfo: TypeAlias = Union[ChunkExtraInfoSchema, StringExtraInfoSchema]


class ExpectedOutputArrayOfFlexibleIoChunk(TypedDict, total=False):
    text: Required[str]

    metadata: object


class ExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(TypedDict, total=False):
    content: Required[str]

    role: Literal["user"]


class ExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(TypedDict, total=False):
    content: Required[str]

    role: Literal["assistant"]


class ExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(TypedDict, total=False):
    content: Required[str]

    role: Literal["system"]


ExpectedOutputArrayOfChatMessageV2: TypeAlias = Union[
    ExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
    ExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
    ExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
]


class ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk(
    TypedDict, total=False
):
    text: Required[str]

    metadata: object


class ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["user"]


class ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["assistant"]


class ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    TypedDict, total=False
):
    content: Required[str]

    role: Literal["system"]


ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2: TypeAlias = Union[
    ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
    ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
    ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
]


class FlexibleTestCaseSchemaParam(TypedDict, total=False):
    input: Required[
        Union[
            str,
            float,
            Iterable[InputArrayOfFlexibleIoChunk],
            Iterable[InputArrayOfChatMessageV2],
            Iterable[object],
            Dict[
                str,
                Union[
                    str,
                    float,
                    Iterable[InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk],
                    Iterable[InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfChatMessageV2],
                    Iterable[object],
                    object,
                ],
            ],
            object,
        ]
    ]

    expected_extra_info: ExpectedExtraInfo

    expected_output: Union[
        str,
        float,
        Iterable[ExpectedOutputArrayOfFlexibleIoChunk],
        Iterable[ExpectedOutputArrayOfChatMessageV2],
        Iterable[object],
        Dict[
            str,
            Union[
                str,
                float,
                Iterable[
                    ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk
                ],
                Iterable[
                    ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2
                ],
                Iterable[object],
                object,
            ],
        ],
        object,
    ]
