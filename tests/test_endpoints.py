"""Tests for API endpoints."""

import pytest
import respx
import httpx

from wordpress_api import WordPressClient
from wordpress_api.models import (
    PostCreate,
    PostUpdate,
    PostStatus,
    PageCreate,
    CategoryCreate,
    TagCreate,
    CommentCreate,
)


class TestPostsEndpoint:
    """Tests for PostsEndpoint."""

    @respx.mock
    def test_list_posts(self, client, api_url, mock_post):
        """Test listing posts."""
        respx.get(f"{api_url}/wp/v2/posts").mock(
            return_value=httpx.Response(200, json=[mock_post])
        )
        
        posts = client.posts.list()
        assert len(posts) == 1
        assert posts[0].id == 1

    @respx.mock
    def test_list_posts_with_filters(self, client, api_url, mock_post):
        """Test listing posts with filters."""
        respx.get(f"{api_url}/wp/v2/posts").mock(
            return_value=httpx.Response(200, json=[mock_post])
        )
        
        posts = client.posts.list(
            status="publish",
            categories=[1],
            per_page=5,
        )
        assert len(posts) == 1

    @respx.mock
    def test_get_post(self, client, api_url, mock_post):
        """Test getting a single post."""
        respx.get(f"{api_url}/wp/v2/posts/1").mock(
            return_value=httpx.Response(200, json=mock_post)
        )
        
        post = client.posts.get(1)
        assert post.id == 1
        assert post.slug == "hello-world"

    @respx.mock
    def test_create_post(self, client, api_url, mock_post):
        """Test creating a post."""
        respx.post(f"{api_url}/wp/v2/posts").mock(
            return_value=httpx.Response(201, json=mock_post)
        )
        
        data = PostCreate(title="Hello World", content="Content")
        post = client.posts.create(data)
        assert post.id == 1

    @respx.mock
    def test_update_post(self, client, api_url, mock_post):
        """Test updating a post."""
        mock_post["title"]["rendered"] = "Updated Title"
        respx.post(f"{api_url}/wp/v2/posts/1").mock(
            return_value=httpx.Response(200, json=mock_post)
        )
        
        data = PostUpdate(title="Updated Title")
        post = client.posts.update(1, data)
        assert post.title.rendered == "Updated Title"

    @respx.mock
    def test_delete_post(self, client, api_url):
        """Test deleting a post."""
        respx.delete(f"{api_url}/wp/v2/posts/1").mock(
            return_value=httpx.Response(200, json={"deleted": True})
        )
        
        result = client.posts.delete(1)
        assert result["deleted"] is True

    @respx.mock
    def test_get_by_slug(self, client, api_url, mock_post):
        """Test getting post by slug."""
        respx.get(f"{api_url}/wp/v2/posts").mock(
            return_value=httpx.Response(200, json=[mock_post])
        )
        
        post = client.posts.get_by_slug("hello-world")
        assert post is not None
        assert post.slug == "hello-world"


class TestPagesEndpoint:
    """Tests for PagesEndpoint."""

    @respx.mock
    def test_list_pages(self, client, api_url, mock_page):
        """Test listing pages."""
        respx.get(f"{api_url}/wp/v2/pages").mock(
            return_value=httpx.Response(200, json=[mock_page])
        )
        
        pages = client.pages.list()
        assert len(pages) == 1
        assert pages[0].id == 10

    @respx.mock
    def test_get_page(self, client, api_url, mock_page):
        """Test getting a single page."""
        respx.get(f"{api_url}/wp/v2/pages/10").mock(
            return_value=httpx.Response(200, json=mock_page)
        )
        
        page = client.pages.get(10)
        assert page.slug == "about"


class TestUsersEndpoint:
    """Tests for UsersEndpoint."""

    @respx.mock
    def test_list_users(self, client, api_url, mock_user):
        """Test listing users."""
        respx.get(f"{api_url}/wp/v2/users").mock(
            return_value=httpx.Response(200, json=[mock_user])
        )
        
        users = client.users.list()
        assert len(users) == 1
        assert users[0].username == "admin"

    @respx.mock
    def test_get_current_user(self, client, api_url, mock_user):
        """Test getting current user."""
        respx.get(f"{api_url}/wp/v2/users/me").mock(
            return_value=httpx.Response(200, json=mock_user)
        )
        
        user = client.users.me()
        assert user.username == "admin"


class TestCommentsEndpoint:
    """Tests for CommentsEndpoint."""

    @respx.mock
    def test_list_comments(self, client, api_url, mock_comment):
        """Test listing comments."""
        respx.get(f"{api_url}/wp/v2/comments").mock(
            return_value=httpx.Response(200, json=[mock_comment])
        )
        
        comments = client.comments.list()
        assert len(comments) == 1
        assert comments[0].author_name == "John Doe"

    @respx.mock
    def test_create_comment(self, client, api_url, mock_comment):
        """Test creating a comment."""
        respx.post(f"{api_url}/wp/v2/comments").mock(
            return_value=httpx.Response(201, json=mock_comment)
        )
        
        data = CommentCreate(post=1, content="Great!")
        comment = client.comments.create(data)
        assert comment.id == 1


class TestCategoriesEndpoint:
    """Tests for CategoriesEndpoint."""

    @respx.mock
    def test_list_categories(self, client, api_url, mock_category):
        """Test listing categories."""
        respx.get(f"{api_url}/wp/v2/categories").mock(
            return_value=httpx.Response(200, json=[mock_category])
        )
        
        categories = client.categories.list()
        assert len(categories) == 1
        assert categories[0].name == "Uncategorized"

    @respx.mock
    def test_create_category(self, client, api_url, mock_category):
        """Test creating a category."""
        respx.post(f"{api_url}/wp/v2/categories").mock(
            return_value=httpx.Response(201, json=mock_category)
        )
        
        data = CategoryCreate(name="Technology")
        category = client.categories.create(data)
        assert category.id == 1


class TestTagsEndpoint:
    """Tests for TagsEndpoint."""

    @respx.mock
    def test_list_tags(self, client, api_url, mock_tag):
        """Test listing tags."""
        respx.get(f"{api_url}/wp/v2/tags").mock(
            return_value=httpx.Response(200, json=[mock_tag])
        )
        
        tags = client.tags.list()
        assert len(tags) == 1
        assert tags[0].name == "Python"


class TestMediaEndpoint:
    """Tests for MediaEndpoint."""

    @respx.mock
    def test_list_media(self, client, api_url, mock_media):
        """Test listing media."""
        respx.get(f"{api_url}/wp/v2/media").mock(
            return_value=httpx.Response(200, json=[mock_media])
        )
        
        media = client.media.list()
        assert len(media) == 1
        assert media[0].media_type == "image"

    @respx.mock
    def test_list_images(self, client, api_url, mock_media):
        """Test listing images."""
        respx.get(f"{api_url}/wp/v2/media").mock(
            return_value=httpx.Response(200, json=[mock_media])
        )
        
        images = client.media.list_images()
        assert len(images) == 1


class TestSearchEndpoint:
    """Tests for SearchEndpoint."""

    @respx.mock
    def test_search(self, client, api_url):
        """Test searching."""
        respx.get(f"{api_url}/wp/v2/search").mock(
            return_value=httpx.Response(200, json=[
                {"id": 1, "title": "Hello", "url": "/hello/", "type": "post", "subtype": "post"}
            ])
        )
        
        results = client.search.search("hello")
        assert len(results) == 1
        assert results[0].title == "Hello"


class TestSettingsEndpoint:
    """Tests for SettingsEndpoint."""

    @respx.mock
    def test_get_settings(self, client, api_url):
        """Test getting settings."""
        respx.get(f"{api_url}/wp/v2/settings").mock(
            return_value=httpx.Response(200, json={
                "title": "My Blog",
                "description": "A WordPress site",
            })
        )
        
        settings = client.settings.get()
        assert settings.title == "My Blog"


class TestTaxonomiesEndpoint:
    """Tests for TaxonomiesEndpoint."""

    @respx.mock
    def test_list_taxonomies(self, client, api_url):
        """Test listing taxonomies."""
        respx.get(f"{api_url}/wp/v2/taxonomies").mock(
            return_value=httpx.Response(200, json={
                "category": {"name": "Categories", "slug": "category"},
                "post_tag": {"name": "Tags", "slug": "post_tag"},
            })
        )
        
        taxonomies = client.taxonomies.list()
        assert "category" in taxonomies
        assert "post_tag" in taxonomies
