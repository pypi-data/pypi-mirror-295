# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Required, Annotated, TypeAlias, TypedDict

from ..._utils import PropertyInfo
from ..token_chunking_strategy_config_param import TokenChunkingStrategyConfigParam
from ..custom_chunking_strategy_config_param import CustomChunkingStrategyConfigParam
from ..character_chunking_strategy_config_param import CharacterChunkingStrategyConfigParam

__all__ = ["UploadScheduleCreateParams", "ChunkingStrategyConfig"]


class UploadScheduleCreateParams(TypedDict, total=False):
    chunking_strategy_config: Required[ChunkingStrategyConfig]

    interval: Required[float]

    knowledge_base_data_source_id: Required[str]

    account_id: str
    """The ID of the account that owns the given entity."""

    next_run_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]


ChunkingStrategyConfig: TypeAlias = Union[
    CharacterChunkingStrategyConfigParam, TokenChunkingStrategyConfigParam, CustomChunkingStrategyConfigParam
]
