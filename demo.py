#!/usr/bin/env python3
"""
WordPress REST API Python Client Demo

This script demonstrates the full capabilities of the WordPress API client.
Run with: python demo.py
"""

import sys
sys.path.insert(0, "src")

from wordpress_api import (
    WordPressClient,
    ApplicationPasswordAuth,
    BasicAuth,
    JWTAuth,
)
from wordpress_api.models import (
    PostCreate,
    PostUpdate,
    PostStatus,
    PageCreate,
    CategoryCreate,
    TagCreate,
    CommentCreate,
    UserCreate,
)


def print_header(title: str) -> None:
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}\n")


def demo_authentication() -> None:
    """Demonstrate authentication methods."""
    print_header("Authentication Methods")
    
    print("1. Application Password Authentication (Recommended)")
    print("   WordPress 5.6+ built-in method for REST API access")
    print("   ")
    print("   auth = ApplicationPasswordAuth('username', 'xxxx xxxx xxxx')")
    print()
    
    print("2. Basic Authentication")
    print("   Works with plugins like 'Application Passwords' or 'Basic Auth'")
    print("   ")
    print("   auth = BasicAuth('username', 'password')")
    print()
    
    print("3. JWT Authentication")
    print("   Requires JWT Authentication plugin")
    print("   ")
    print("   auth = JWTAuth()")
    print("   auth.obtain_token(client, 'username', 'password')")
    print()


def demo_client_setup() -> None:
    """Demonstrate client initialization."""
    print_header("Client Setup")
    
    print("Basic setup:")
    print("```python")
    print("from wordpress_api import WordPressClient, ApplicationPasswordAuth")
    print()
    print("# With authentication")
    print("auth = ApplicationPasswordAuth('admin', 'xxxx xxxx xxxx xxxx')")
    print("client = WordPressClient('https://example.com', auth=auth)")
    print()
    print("# Without authentication (public endpoints only)")
    print("client = WordPressClient('https://example.com')")
    print()
    print("# Context manager (auto-close)")
    print("with WordPressClient('https://example.com', auth=auth) as client:")
    print("    posts = client.posts.list()")
    print("```")
    print()


def demo_posts_api() -> None:
    """Demonstrate Posts API."""
    print_header("Posts API")
    
    print("List posts:")
    print("```python")
    print("# Get recent posts")
    print("posts = client.posts.list()")
    print()
    print("# With filtering")
    print("posts = client.posts.list(")
    print("    status='publish',")
    print("    categories=[1, 5],")
    print("    tags=[10],")
    print("    per_page=20,")
    print("    search='hello'")
    print(")")
    print()
    print("# Iterate through all posts")
    print("for post in client.posts.iterate_all():")
    print("    print(post.title.rendered)")
    print("```")
    print()
    
    print("Create a post:")
    print("```python")
    print("from wordpress_api.models import PostCreate, PostStatus")
    print()
    print("new_post = client.posts.create(PostCreate(")
    print("    title='My New Post',")
    print("    content='<p>Hello World!</p>',")
    print("    status=PostStatus.PUBLISH,")
    print("    categories=[1],")
    print("    tags=[2, 3]")
    print("))")
    print("```")
    print()
    
    print("Update a post:")
    print("```python")
    print("updated = client.posts.update(123, PostUpdate(")
    print("    title='Updated Title',")
    print("    content='Updated content'")
    print("))")
    print("```")
    print()
    
    print("Delete a post:")
    print("```python")
    print("# Move to trash")
    print("client.posts.trash(123)")
    print()
    print("# Permanently delete")
    print("client.posts.delete(123, force=True)")
    print("```")
    print()


def demo_pages_api() -> None:
    """Demonstrate Pages API."""
    print_header("Pages API")
    
    print("```python")
    print("# List pages")
    print("pages = client.pages.list(order='asc', orderby='menu_order')")
    print()
    print("# Get page hierarchy")
    print("hierarchy = client.pages.get_hierarchy()")
    print("root_pages = hierarchy.get(0, [])")
    print()
    print("# Get child pages")
    print("children = client.pages.get_children(parent_id=42)")
    print()
    print("# Create a page")
    print("page = client.pages.create(PageCreate(")
    print("    title='About Us',")
    print("    content='<p>Company info here</p>',")
    print("    parent=0,")
    print("    menu_order=1")
    print("))")
    print("```")
    print()


def demo_media_api() -> None:
    """Demonstrate Media API."""
    print_header("Media API")
    
    print("Upload media:")
    print("```python")
    print("# Upload from file path")
    print("media = client.media.upload(")
    print("    'path/to/image.jpg',")
    print("    title='My Image',")
    print("    alt_text='Description of the image'")
    print(")")
    print()
    print("# Upload from file object")
    print("with open('image.png', 'rb') as f:")
    print("    media = client.media.upload(f, filename='image.png')")
    print("```")
    print()
    
    print("List media:")
    print("```python")
    print("# All media")
    print("all_media = client.media.list()")
    print()
    print("# Only images")
    print("images = client.media.list_images()")
    print()
    print("# Only videos")
    print("videos = client.media.list_videos()")
    print()
    print("# Get image sizes")
    print("sizes = client.media.get_sizes(media_id=123)")
    print("```")
    print()


def demo_users_api() -> None:
    """Demonstrate Users API."""
    print_header("Users API")
    
    print("```python")
    print("# Get current user")
    print("me = client.users.me()")
    print("print(f'Logged in as: {me.name}')")
    print()
    print("# List users")
    print("users = client.users.list()")
    print()
    print("# List by role")
    print("editors = client.users.list_by_role('editor')")
    print()
    print("# List authors (users with published posts)")
    print("authors = client.users.list_authors()")
    print()
    print("# Create user")
    print("user = client.users.create(UserCreate(")
    print("    username='newuser',")
    print("    email='newuser@example.com',")
    print("    password='securepassword123',")
    print("    roles=['author']")
    print("))")
    print("```")
    print()


def demo_comments_api() -> None:
    """Demonstrate Comments API."""
    print_header("Comments API")
    
    print("```python")
    print("# List comments for a post")
    print("comments = client.comments.list_for_post(post_id=123)")
    print()
    print("# Get comment thread (organized by parent)")
    print("thread = client.comments.get_thread(post_id=123)")
    print("top_level = thread.get(0, [])")
    print()
    print("# Create a comment")
    print("comment = client.comments.create(CommentCreate(")
    print("    post=123,")
    print("    content='Great article!',")
    print("    author_name='John Doe',")
    print("    author_email='john@example.com'")
    print("))")
    print()
    print("# Moderate comments")
    print("client.comments.approve(456)")
    print("client.comments.unapprove(456)")
    print("client.comments.spam(456)")
    print("client.comments.trash(456)")
    print("```")
    print()


def demo_categories_tags_api() -> None:
    """Demonstrate Categories and Tags API."""
    print_header("Categories & Tags API")
    
    print("Categories:")
    print("```python")
    print("# List categories")
    print("categories = client.categories.list()")
    print()
    print("# Get category hierarchy")
    print("hierarchy = client.categories.get_hierarchy()")
    print()
    print("# Create category")
    print("cat = client.categories.create(CategoryCreate(")
    print("    name='Technology',")
    print("    description='Tech articles',")
    print("    parent=0")
    print("))")
    print("```")
    print()
    
    print("Tags:")
    print("```python")
    print("# List tags")
    print("tags = client.tags.list()")
    print()
    print("# Get popular tags")
    print("popular = client.tags.get_popular(limit=20)")
    print()
    print("# Create tag")
    print("tag = client.tags.create(TagCreate(name='Python'))")
    print("```")
    print()


def demo_search_api() -> None:
    """Demonstrate Search API."""
    print_header("Search API")
    
    print("```python")
    print("# Search everything")
    print("results = client.search.search('wordpress')")
    print()
    print("# Search only posts")
    print("posts = client.search.search_posts('tutorial')")
    print()
    print("# Search only pages")
    print("pages = client.search.search_pages('about')")
    print()
    print("# Search categories")
    print("categories = client.search.search_categories('tech')")
    print("```")
    print()


def demo_settings_api() -> None:
    """Demonstrate Settings API."""
    print_header("Settings API (Admin only)")
    
    print("```python")
    print("# Get all settings")
    print("settings = client.settings.get()")
    print("print(f'Site title: {settings.title}')")
    print("print(f'Tagline: {settings.description}')")
    print()
    print("# Update settings")
    print("client.settings.update(")
    print("    title='My Awesome Blog',")
    print("    description='A blog about awesome things'")
    print(")")
    print("```")
    print()


def demo_plugins_themes_api() -> None:
    """Demonstrate Plugins and Themes API."""
    print_header("Plugins & Themes API (Admin only)")
    
    print("Plugins:")
    print("```python")
    print("# List plugins")
    print("plugins = client.plugins.list()")
    print()
    print("# List active plugins")
    print("active = client.plugins.list_active()")
    print()
    print("# Activate/deactivate plugin")
    print("client.plugins.activate('akismet/akismet')")
    print("client.plugins.deactivate('akismet/akismet')")
    print("```")
    print()
    
    print("Themes:")
    print("```python")
    print("# List themes")
    print("themes = client.themes.list()")
    print()
    print("# Get active theme")
    print("active = client.themes.get_active()")
    print("print(f'Current theme: {active.name}')")
    print("```")
    print()


def demo_menus_api() -> None:
    """Demonstrate Menus API."""
    print_header("Navigation Menus API")
    
    print("```python")
    print("# List menus")
    print("menus = client.menus.list_menus()")
    print()
    print("# Get menu items")
    print("items = client.menus.get_menu_items(menu_id=1)")
    print()
    print("# List menu locations")
    print("locations = client.menus.list_locations()")
    print()
    print("# Create menu item")
    print("from wordpress_api.models import MenuItemCreate")
    print("item = client.menus.create_item(MenuItemCreate(")
    print("    title='Home',")
    print("    url='/',")
    print("    menus=1")
    print("))")
    print("```")
    print()


def demo_blocks_api() -> None:
    """Demonstrate Blocks API."""
    print_header("Block Editor API")
    
    print("```python")
    print("# List block types")
    print("blocks = client.blocks.list_types()")
    print()
    print("# List core blocks")
    print("core_blocks = client.blocks.list_core_blocks()")
    print()
    print("# Get specific block type")
    print("paragraph = client.blocks.get_type('core', 'paragraph')")
    print()
    print("# List block patterns")
    print("patterns = client.blocks.list_patterns()")
    print()
    print("# List pattern categories")
    print("categories = client.blocks.list_pattern_categories()")
    print("```")
    print()


def demo_revisions_api() -> None:
    """Demonstrate Revisions API."""
    print_header("Revisions & Autosaves API")
    
    print("Revisions:")
    print("```python")
    print("# List post revisions")
    print("revisions = client.revisions.list_post_revisions(post_id=123)")
    print()
    print("# Get latest revision")
    print("latest = client.revisions.get_latest_revision(post_id=123)")
    print()
    print("# Delete a revision")
    print("client.revisions.delete_post_revision(post_id=123, revision_id=456)")
    print("```")
    print()
    
    print("Autosaves:")
    print("```python")
    print("# List autosaves")
    print("autosaves = client.autosaves.list_post_autosaves(post_id=123)")
    print()
    print("# Create autosave")
    print("autosave = client.autosaves.create_post_autosave(")
    print("    post_id=123,")
    print("    title='Draft title',")
    print("    content='Work in progress...'")
    print(")")
    print("```")
    print()


def demo_custom_post_types() -> None:
    """Demonstrate Custom Post Types."""
    print_header("Custom Post Types")
    
    print("```python")
    print("# Access a custom post type (e.g., 'products')")
    print("products = client.custom_post_type('products')")
    print()
    print("# List items")
    print("all_products = products.list()")
    print()
    print("# Get single item")
    print("product = products.get(123)")
    print()
    print("# Create item")
    print("new_product = products.create({")
    print("    'title': 'New Product',")
    print("    'content': 'Product description',")
    print("    'status': 'publish',")
    print("    'meta': {'price': '99.99'}")
    print("})")
    print()
    print("# Update item")
    print("products.update(123, {'title': 'Updated Product'})")
    print("```")
    print()


def demo_pagination() -> None:
    """Demonstrate pagination helpers."""
    print_header("Pagination")
    
    print("```python")
    print("# Get paginated results")
    print("posts = client.posts.list(page=1, per_page=10)")
    print()
    print("# Access pagination info")
    print("print(f'Total items: {client.total_items}')")
    print("print(f'Total pages: {client.total_pages}')")
    print()
    print("# Iterate through all items automatically")
    print("for post in client.posts.iterate_all(per_page=100):")
    print("    print(post.title.rendered)")
    print("```")
    print()


def demo_error_handling() -> None:
    """Demonstrate error handling."""
    print_header("Error Handling")
    
    print("```python")
    print("from wordpress_api import (")
    print("    WordPressError,")
    print("    AuthenticationError,")
    print("    NotFoundError,")
    print("    ValidationError,")
    print("    RateLimitError,")
    print(")")
    print()
    print("try:")
    print("    post = client.posts.get(99999)")
    print("except NotFoundError as e:")
    print("    print(f'Post not found: {e.message}')")
    print("except AuthenticationError as e:")
    print("    print(f'Auth failed: {e.message}')")
    print("except ValidationError as e:")
    print("    print(f'Invalid data: {e.message}')")
    print("except RateLimitError as e:")
    print("    print(f'Rate limited, retry later')")
    print("except WordPressError as e:")
    print("    print(f'API error: {e.message} [{e.status_code}]')")
    print("```")
    print()


def main() -> None:
    """Run all demos."""
    print("\n" + "="*60)
    print(" WordPress REST API Python Client")
    print(" Full-Featured Interface for Python 3.12")
    print("="*60)
    
    demo_authentication()
    demo_client_setup()
    demo_posts_api()
    demo_pages_api()
    demo_media_api()
    demo_users_api()
    demo_comments_api()
    demo_categories_tags_api()
    demo_search_api()
    demo_settings_api()
    demo_plugins_themes_api()
    demo_menus_api()
    demo_blocks_api()
    demo_revisions_api()
    demo_custom_post_types()
    demo_pagination()
    demo_error_handling()
    
    print_header("Quick Start Example")
    print("```python")
    print("from wordpress_api import WordPressClient, ApplicationPasswordAuth")
    print("from wordpress_api.models import PostCreate, PostStatus")
    print()
    print("# Connect to WordPress")
    print("auth = ApplicationPasswordAuth('admin', 'xxxx xxxx xxxx xxxx')")
    print("client = WordPressClient('https://your-site.com', auth=auth)")
    print()
    print("# Create a post")
    print("post = client.posts.create(PostCreate(")
    print("    title='Hello from Python!',")
    print("    content='<p>This post was created via the REST API.</p>',")
    print("    status=PostStatus.PUBLISH")
    print("))")
    print()
    print("print(f'Created post #{post.id}: {post.title.rendered}')")
    print("```")
    print()
    
    print("="*60)
    print(" Available Endpoints:")
    print("="*60)
    print()
    endpoints = [
        ("client.posts", "Posts (CRUD, filter, trash/restore)"),
        ("client.pages", "Pages (CRUD, hierarchy, children)"),
        ("client.media", "Media (upload, CRUD, sizes)"),
        ("client.users", "Users (CRUD, me, roles)"),
        ("client.comments", "Comments (CRUD, moderation, threads)"),
        ("client.categories", "Categories (CRUD, hierarchy)"),
        ("client.tags", "Tags (CRUD, popular)"),
        ("client.taxonomies", "Taxonomies (list, get)"),
        ("client.settings", "Site Settings (get, update)"),
        ("client.plugins", "Plugins (list, activate, deactivate)"),
        ("client.themes", "Themes (list, get active)"),
        ("client.menus", "Menus & Menu Items (CRUD)"),
        ("client.search", "Site-wide Search"),
        ("client.blocks", "Block Types & Patterns"),
        ("client.revisions", "Post/Page Revisions"),
        ("client.autosaves", "Post/Page Autosaves"),
        ("client.custom_post_type()", "Custom Post Types"),
        ("client.post_types", "Post Types Registry"),
        ("client.statuses", "Post Statuses Registry"),
    ]
    
    for endpoint, description in endpoints:
        print(f"  {endpoint:<30} - {description}")
    
    print()
    print("="*60)
    print(" For more information, see the source code in src/wordpress_api/")
    print("="*60)
    print()


if __name__ == "__main__":
    main()
