"""Taxonomy models."""

from typing import Any

from pydantic import Field

from .base import WordPressModel


class TaxonomyLabels(WordPressModel):
    """Labels for a taxonomy."""

    name: str = ""
    singular_name: str = ""
    search_items: str = ""
    popular_items: str | None = None
    all_items: str = ""
    parent_item: str | None = None
    parent_item_colon: str | None = None
    edit_item: str = ""
    view_item: str = ""
    update_item: str = ""
    add_new_item: str = ""
    new_item_name: str = ""
    separate_items_with_commas: str | None = None
    add_or_remove_items: str | None = None
    choose_from_most_used: str | None = None
    not_found: str = ""
    no_terms: str = ""
    items_list_navigation: str = ""
    items_list: str = ""
    most_used: str = ""
    back_to_items: str = ""


class Taxonomy(WordPressModel):
    """WordPress Taxonomy object."""

    name: str = ""
    slug: str = ""
    description: str = ""
    types: list[str] = Field(default_factory=list)
    hierarchical: bool = False
    rest_base: str = ""
    rest_namespace: str = "wp/v2"
    labels: TaxonomyLabels | None = None
    show_cloud: bool = False
    visibility: dict[str, bool] = Field(default_factory=dict)
    capabilities: dict[str, str] = Field(default_factory=dict)
