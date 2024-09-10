# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Required, Annotated, TypeAlias, TypedDict

from ..._utils import PropertyInfo
from ..token_chunking_strategy_config_param import TokenChunkingStrategyConfigParam
from ..custom_chunking_strategy_config_param import CustomChunkingStrategyConfigParam
from ..character_chunking_strategy_config_param import CharacterChunkingStrategyConfigParam

__all__ = ["UploadScheduleUpdateParams", "ChunkingStrategyConfig"]


class UploadScheduleUpdateParams(TypedDict, total=False):
    knowledge_base_id: Required[str]

    chunking_strategy_config: ChunkingStrategyConfig

    interval: float

    next_run_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]


ChunkingStrategyConfig: TypeAlias = Union[
    CharacterChunkingStrategyConfigParam, TokenChunkingStrategyConfigParam, CustomChunkingStrategyConfigParam
]
