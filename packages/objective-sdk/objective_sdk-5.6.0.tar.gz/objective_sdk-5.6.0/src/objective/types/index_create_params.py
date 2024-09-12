# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = [
    "IndexCreateParams",
    "Configuration",
    "ConfigurationFields",
    "ConfigurationFieldsSearchable",
    "ConfigurationFieldsCrawlable",
    "ConfigurationFieldsFilterable",
    "ConfigurationIndexType",
    "ConfigurationIndexTypeFinetuning",
    "ConfigurationIndexTypeFinetuningFeedback",
    "ConfigurationIndexTypeHighlights",
]


class IndexCreateParams(TypedDict, total=False):
    configuration: Required[Configuration]


class ConfigurationFieldsSearchable(TypedDict, total=False):
    allow: Required[List[str]]

    deny: List[str]


class ConfigurationFieldsCrawlable(TypedDict, total=False):
    allow: List[str]

    deny: List[str]


class ConfigurationFieldsFilterable(TypedDict, total=False):
    allow: List[str]

    deny: Union[List[str], List[str]]


class ConfigurationFields(TypedDict, total=False):
    searchable: Required[ConfigurationFieldsSearchable]

    crawlable: ConfigurationFieldsCrawlable

    filterable: ConfigurationFieldsFilterable

    segment_delimiter: Dict[str, object]

    types: Dict[str, str]


class ConfigurationIndexTypeFinetuningFeedback(TypedDict, total=False):
    query: Required[str]

    label: Literal["GREAT", "OK", "BAD"]

    object_id: str


class ConfigurationIndexTypeFinetuning(TypedDict, total=False):
    base_index_id: Required[str]

    feedback: Required[Iterable[ConfigurationIndexTypeFinetuningFeedback]]


class ConfigurationIndexTypeHighlights(TypedDict, total=False):
    text: bool


class ConfigurationIndexType(TypedDict, total=False):
    name: Required[
        Literal[
            "multimodal",
            "text",
            "text-rainbow",
            "multimodal-hybrid",
            "multimodal-hybrid-6-shards",
            "multimodal-hybrid-12-shards",
            "text-hybrid",
            "turbo-only",
            "turbo-only-with-6-shards",
            "turbo-only-with-12-shards",
            "turbo-only-with-24-shards",
            "image",
        ]
    ]

    finetuning: ConfigurationIndexTypeFinetuning

    highlights: ConfigurationIndexTypeHighlights

    version: str


class Configuration(TypedDict, total=False):
    fields: Required[ConfigurationFields]

    index_type: ConfigurationIndexType
