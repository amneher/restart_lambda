"""WordPress REST API Endpoints."""

from .posts import PostsEndpoint
from .pages import PagesEndpoint
from .media import MediaEndpoint
from .users import UsersEndpoint
from .comments import CommentsEndpoint
from .categories import CategoriesEndpoint
from .tags import TagsEndpoint
from .taxonomies import TaxonomiesEndpoint
from .settings import SettingsEndpoint
from .plugins import PluginsEndpoint
from .themes import ThemesEndpoint
from .menus import MenusEndpoint
from .search import SearchEndpoint
from .blocks import BlocksEndpoint
from .revisions import RevisionsEndpoint
from .autosaves import AutosavesEndpoint
from .post_types import PostTypesEndpoint
from .statuses import StatusesEndpoint
from .application_passwords import ApplicationPasswordsEndpoint

__all__ = [
    "PostsEndpoint",
    "PagesEndpoint",
    "MediaEndpoint",
    "UsersEndpoint",
    "CommentsEndpoint",
    "CategoriesEndpoint",
    "TagsEndpoint",
    "TaxonomiesEndpoint",
    "SettingsEndpoint",
    "PluginsEndpoint",
    "ThemesEndpoint",
    "MenusEndpoint",
    "SearchEndpoint",
    "BlocksEndpoint",
    "RevisionsEndpoint",
    "AutosavesEndpoint",
    "PostTypesEndpoint",
    "StatusesEndpoint",
    "ApplicationPasswordsEndpoint",
]
