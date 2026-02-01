# WordPress REST API Python Client

A full-featured Python 3.12 interface to the WordPress REST API.

## Overview

This library provides a comprehensive, type-safe Python client for interacting with WordPress sites via the REST API. It supports all major WordPress endpoints including posts, pages, media, users, comments, categories, tags, settings, plugins, themes, menus, and more.

## Project Structure

```
src/wordpress_api/
├── __init__.py          # Main exports
├── client.py            # WordPressClient main class
├── auth.py              # Authentication handlers
├── exceptions.py        # Custom exceptions
├── models/              # Pydantic data models
│   ├── post.py
│   ├── page.py
│   ├── media.py
│   ├── user.py
│   ├── comment.py
│   ├── category.py
│   ├── tag.py
│   └── ...
└── endpoints/           # API endpoint classes
    ├── posts.py
    ├── pages.py
    ├── media.py
    ├── users.py
    ├── comments.py
    └── ...
```

## Quick Start

```python
from wordpress_api import WordPressClient, ApplicationPasswordAuth

# Authenticate with WordPress Application Passwords
auth = ApplicationPasswordAuth("username", "xxxx xxxx xxxx xxxx")
client = WordPressClient("https://your-site.com", auth=auth)

# List posts
posts = client.posts.list()

# Create a post
from wordpress_api.models import PostCreate, PostStatus
post = client.posts.create(PostCreate(
    title="Hello World",
    content="<p>My first post!</p>",
    status=PostStatus.PUBLISH
))

# Get current user
me = client.users.me()
```

## Features

- **Full CRUD Support**: Posts, Pages, Media, Users, Comments, Categories, Tags
- **Authentication**: Application Passwords, Basic Auth, JWT
- **Type Safety**: Pydantic models for all WordPress objects
- **Pagination**: Automatic iteration through all results
- **Media Upload**: Upload files from path or file objects
- **Custom Post Types**: Access any registered custom post type
- **Block Editor**: Access block types and patterns
- **Error Handling**: Typed exceptions for all API errors

## Running the Demo

```bash
python demo.py
```

## Dependencies

- httpx: Modern HTTP client
- pydantic: Data validation using Python type annotations

## Authentication Setup

1. Go to your WordPress site
2. Navigate to Users → Your Profile
3. Scroll to "Application Passwords"
4. Create a new application password
5. Use it with `ApplicationPasswordAuth`
