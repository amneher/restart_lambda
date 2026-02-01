"""Block Types and Patterns endpoints."""

from typing import Any

from pydantic import BaseModel, Field

from .base import BaseEndpoint


class BlockType(BaseModel):
    """WordPress Block Type."""

    name: str = ""
    title: str = ""
    description: str = ""
    icon: str | None = None
    category: str = ""
    keywords: list[str] = Field(default_factory=list)
    parent: list[str] | None = None
    supports: dict[str, Any] = Field(default_factory=dict)
    styles: list[dict[str, Any]] = Field(default_factory=list)
    textdomain: str = ""
    example: dict[str, Any] | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)
    provides_context: dict[str, str] = Field(default_factory=dict)
    uses_context: list[str] = Field(default_factory=list)
    editor_script: str | None = None
    script: str | None = None
    editor_style: str | None = None
    style: str | None = None
    is_dynamic: bool = False
    api_version: int = 1


class BlockPattern(BaseModel):
    """WordPress Block Pattern."""

    name: str = ""
    title: str = ""
    description: str = ""
    content: str = ""
    categories: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    viewport_width: int | None = None
    block_types: list[str] = Field(default_factory=list)
    inserter: bool = True


class BlockPatternCategory(BaseModel):
    """WordPress Block Pattern Category."""

    name: str = ""
    label: str = ""
    description: str = ""


class BlocksEndpoint(BaseEndpoint):
    """Endpoint for WordPress block types and patterns."""

    _types_path = "/wp/v2/block-types"
    _patterns_path = "/wp/v2/block-patterns/patterns"
    _pattern_categories_path = "/wp/v2/block-patterns/categories"

    def list_types(self, namespace: str | None = None, **kwargs: Any) -> list[BlockType]:
        """List registered block types.
        
        Args:
            namespace: Filter by block namespace (e.g., 'core').
        """
        params: dict[str, Any] = {}
        if namespace:
            params["namespace"] = namespace
        params.update(kwargs)
        
        response = self._get(self._types_path, params=params)
        return [BlockType.model_validate(item) for item in response]

    def get_type(self, namespace: str, name: str, **kwargs: Any) -> BlockType:
        """Get a specific block type.
        
        Args:
            namespace: Block namespace (e.g., 'core').
            name: Block name (e.g., 'paragraph').
        """
        response = self._get(f"{self._types_path}/{namespace}/{name}", params=kwargs)
        return BlockType.model_validate(response)

    def list_core_blocks(self) -> list[BlockType]:
        """List all core WordPress blocks."""
        return self.list_types(namespace="core")

    def list_patterns(self, **kwargs: Any) -> list[BlockPattern]:
        """List registered block patterns."""
        response = self._get(self._patterns_path, params=kwargs)
        return [BlockPattern.model_validate(item) for item in response]

    def list_pattern_categories(self, **kwargs: Any) -> list[BlockPatternCategory]:
        """List block pattern categories."""
        response = self._get(self._pattern_categories_path, params=kwargs)
        return [BlockPatternCategory.model_validate(item) for item in response]

    def get_patterns_by_category(self, category: str) -> list[BlockPattern]:
        """Get patterns filtered by category."""
        patterns = self.list_patterns()
        return [p for p in patterns if category in p.categories]
