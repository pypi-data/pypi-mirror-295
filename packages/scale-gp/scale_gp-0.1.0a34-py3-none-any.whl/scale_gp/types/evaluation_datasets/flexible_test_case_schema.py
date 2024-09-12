# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from ..shared.chunk_extra_info_schema import ChunkExtraInfoSchema
from ..shared.string_extra_info_schema import StringExtraInfoSchema

__all__ = [
    "FlexibleTestCaseSchema",
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


class InputArrayOfFlexibleIoChunk(BaseModel):
    text: str

    metadata: Optional[object] = None


class InputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(BaseModel):
    content: str

    role: Optional[Literal["user"]] = None


class InputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(BaseModel):
    content: str

    role: Optional[Literal["assistant"]] = None


class InputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(BaseModel):
    content: str

    role: Optional[Literal["system"]] = None


InputArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        InputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        InputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        InputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk(BaseModel):
    text: str

    metadata: Optional[object] = None


class InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]

ExpectedExtraInfo: TypeAlias = Annotated[
    Union[ChunkExtraInfoSchema, StringExtraInfoSchema], PropertyInfo(discriminator="schema_type")
]


class ExpectedOutputArrayOfFlexibleIoChunk(BaseModel):
    text: str

    metadata: Optional[object] = None


class ExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(BaseModel):
    content: str

    role: Optional[Literal["user"]] = None


class ExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(BaseModel):
    content: str

    role: Optional[Literal["assistant"]] = None


class ExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(BaseModel):
    content: str

    role: Optional[Literal["system"]] = None


ExpectedOutputArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        ExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        ExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        ExpectedOutputArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk(BaseModel):
    text: str

    metadata: Optional[object] = None


class ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["user"]] = None


class ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["assistant"]] = None


class ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage(
    BaseModel
):
    content: str

    role: Optional[Literal["system"]] = None


ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2: TypeAlias = Annotated[
    Union[
        ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesUserMessage,
        ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesAssistantMessage,
        ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2EgpAPIBackendServerInternalEntitiesSystemMessage,
    ],
    PropertyInfo(discriminator="role"),
]


class FlexibleTestCaseSchema(BaseModel):
    input: Union[
        str,
        float,
        List[InputArrayOfFlexibleIoChunk],
        List[InputArrayOfChatMessageV2],
        List[object],
        Dict[
            str,
            Union[
                str,
                float,
                List[InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk],
                List[InputSomeAdditionalPropertiesInputSomeAdditionalPropertiesItemArrayOfChatMessageV2],
                List[object],
                object,
            ],
        ],
        object,
    ]

    expected_extra_info: Optional[ExpectedExtraInfo] = None

    expected_output: Union[
        str,
        float,
        List[ExpectedOutputArrayOfFlexibleIoChunk],
        List[ExpectedOutputArrayOfChatMessageV2],
        List[object],
        Dict[
            str,
            Union[
                str,
                float,
                List[
                    ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfFlexibleIoChunk
                ],
                List[
                    ExpectedOutputSomeAdditionalPropertiesExpectedOutputSomeAdditionalPropertiesItemArrayOfChatMessageV2
                ],
                List[object],
                object,
            ],
        ],
        object,
        None,
    ] = None
