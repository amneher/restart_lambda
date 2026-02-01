"""Tests for Pydantic models."""

import pytest
from datetime import datetime

from wordpress_api.models import (
    Post,
    PostCreate,
    PostUpdate,
    PostStatus,
    PostFormat,
    Page,
    PageCreate,
    PageUpdate,
    Media,
    MediaCreate,
    User,
    UserCreate,
    UserUpdate,
    Comment,
    CommentCreate,
    CommentStatus,
    Category,
    CategoryCreate,
    Tag,
    TagCreate,
    Taxonomy,
    Settings,
    Plugin,
    Theme,
    Menu,
    MenuItem,
)


class TestPostModels:
    """Tests for Post models."""

    def test_post_from_dict(self, mock_post):
        """Test Post model validation from dict."""
        post = Post.model_validate(mock_post)
        assert post.id == 1
        assert post.slug == "hello-world"
        assert post.status == PostStatus.PUBLISH
        assert post.title.rendered == "Hello World"

    def test_post_date_parsing(self, mock_post):
        """Test that dates are parsed correctly."""
        post = Post.model_validate(mock_post)
        assert isinstance(post.date, datetime)
        assert isinstance(post.modified, datetime)

    def test_post_create(self):
        """Test PostCreate model."""
        data = PostCreate(
            title="New Post",
            content="<p>Content here</p>",
            status=PostStatus.DRAFT,
        )
        assert data.title == "New Post"
        assert data.status == PostStatus.DRAFT

    def test_post_update(self):
        """Test PostUpdate model."""
        data = PostUpdate(title="Updated Title")
        assert data.title == "Updated Title"
        assert data.content is None

    def test_post_status_enum(self):
        """Test PostStatus enum values."""
        assert PostStatus.PUBLISH.value == "publish"
        assert PostStatus.DRAFT.value == "draft"
        assert PostStatus.PENDING.value == "pending"
        assert PostStatus.PRIVATE.value == "private"

    def test_post_format_enum(self):
        """Test PostFormat enum values."""
        assert PostFormat.STANDARD.value == "standard"
        assert PostFormat.GALLERY.value == "gallery"
        assert PostFormat.VIDEO.value == "video"


class TestPageModels:
    """Tests for Page models."""

    def test_page_from_dict(self, mock_page):
        """Test Page model validation from dict."""
        page = Page.model_validate(mock_page)
        assert page.id == 10
        assert page.slug == "about"
        assert page.type == "page"

    def test_page_create(self):
        """Test PageCreate model."""
        data = PageCreate(
            title="About Page",
            content="<p>About us</p>",
            parent=0,
        )
        assert data.title == "About Page"
        assert data.parent == 0


class TestUserModels:
    """Tests for User models."""

    def test_user_from_dict(self, mock_user):
        """Test User model validation from dict."""
        user = User.model_validate(mock_user)
        assert user.id == 1
        assert user.username == "admin"
        assert user.email == "admin@example.com"
        assert "administrator" in user.roles

    def test_user_create(self):
        """Test UserCreate model."""
        data = UserCreate(
            username="newuser",
            email="new@example.com",
            password="securepass123",
        )
        assert data.username == "newuser"
        assert data.email == "new@example.com"

    def test_user_update(self):
        """Test UserUpdate model."""
        data = UserUpdate(first_name="John", last_name="Doe")
        assert data.first_name == "John"
        assert data.password is None


class TestMediaModels:
    """Tests for Media models."""

    def test_media_from_dict(self, mock_media):
        """Test Media model validation from dict."""
        media = Media.model_validate(mock_media)
        assert media.id == 100
        assert media.media_type == "image"
        assert media.mime_type == "image/jpeg"

    def test_media_create(self):
        """Test MediaCreate model."""
        data = MediaCreate(
            title="My Image",
            alt_text="Description",
        )
        assert data.title == "My Image"
        assert data.alt_text == "Description"


class TestCommentModels:
    """Tests for Comment models."""

    def test_comment_from_dict(self, mock_comment):
        """Test Comment model validation from dict."""
        comment = Comment.model_validate(mock_comment)
        assert comment.id == 1
        assert comment.post == 1
        assert comment.author_name == "John Doe"

    def test_comment_create(self):
        """Test CommentCreate model."""
        data = CommentCreate(
            post=1,
            content="Great article!",
            author_name="Jane Doe",
            author_email="jane@example.com",
        )
        assert data.post == 1
        assert data.content == "Great article!"

    def test_comment_status_enum(self):
        """Test CommentStatus enum values."""
        assert CommentStatus.APPROVED.value == "approved"
        assert CommentStatus.HOLD.value == "hold"
        assert CommentStatus.SPAM.value == "spam"


class TestCategoryModels:
    """Tests for Category models."""

    def test_category_from_dict(self, mock_category):
        """Test Category model validation from dict."""
        category = Category.model_validate(mock_category)
        assert category.id == 1
        assert category.name == "Uncategorized"
        assert category.count == 5

    def test_category_create(self):
        """Test CategoryCreate model."""
        data = CategoryCreate(
            name="Technology",
            description="Tech posts",
        )
        assert data.name == "Technology"


class TestTagModels:
    """Tests for Tag models."""

    def test_tag_from_dict(self, mock_tag):
        """Test Tag model validation from dict."""
        tag = Tag.model_validate(mock_tag)
        assert tag.id == 1
        assert tag.name == "Python"
        assert tag.count == 3

    def test_tag_create(self):
        """Test TagCreate model."""
        data = TagCreate(name="JavaScript")
        assert data.name == "JavaScript"


class TestOtherModels:
    """Tests for other models."""

    def test_taxonomy_model(self):
        """Test Taxonomy model."""
        data = {
            "name": "Categories",
            "slug": "category",
            "hierarchical": True,
        }
        taxonomy = Taxonomy.model_validate(data)
        assert taxonomy.name == "Categories"
        assert taxonomy.hierarchical is True

    def test_settings_model(self):
        """Test Settings model."""
        data = {
            "title": "My Blog",
            "description": "A WordPress blog",
            "timezone": "UTC",
        }
        settings = Settings.model_validate(data)
        assert settings.title == "My Blog"

    def test_plugin_model(self):
        """Test Plugin model."""
        data = {
            "plugin": "akismet/akismet",
            "status": "active",
            "name": "Akismet",
            "version": "5.0",
        }
        plugin = Plugin.model_validate(data)
        assert plugin.name == "Akismet"
        assert plugin.status == "active"

    def test_theme_model(self):
        """Test Theme model."""
        data = {
            "stylesheet": "twentytwentyfour",
            "template": "twentytwentyfour",
            "status": "active",
            "version": "1.0",
        }
        theme = Theme.model_validate(data)
        assert theme.stylesheet == "twentytwentyfour"

    def test_menu_model(self):
        """Test Menu model."""
        data = {
            "id": 1,
            "name": "Main Menu",
            "slug": "main-menu",
        }
        menu = Menu.model_validate(data)
        assert menu.name == "Main Menu"

    def test_menu_item_model(self):
        """Test MenuItem model."""
        data = {
            "id": 1,
            "title": "Home",
            "url": "/",
            "menu_order": 1,
        }
        item = MenuItem.model_validate(data)
        assert item.title == "Home"
