"""Media endpoint."""

from pathlib import Path
from typing import Any, BinaryIO

from ..models.media import Media, MediaCreate, MediaUpdate
from .base import CRUDEndpoint


class MediaEndpoint(CRUDEndpoint[Media]):
    """Endpoint for managing WordPress media files."""

    _path = "/wp/v2/media"
    _model_class = Media

    def list(
        self,
        page: int = 1,
        per_page: int = 10,
        search: str | None = None,
        order: str = "desc",
        orderby: str = "date",
        media_type: str | None = None,
        mime_type: str | None = None,
        author: int | list[int] | None = None,
        author_exclude: list[int] | None = None,
        before: str | None = None,
        after: str | None = None,
        parent: int | list[int] | None = None,
        parent_exclude: list[int] | None = None,
        status: str | None = None,
        slug: str | list[str] | None = None,
        **kwargs: Any,
    ) -> list[Media]:
        """List media items with filtering options."""
        params: dict[str, Any] = {
            "page": page,
            "per_page": per_page,
            "order": order,
            "orderby": orderby,
        }
        
        if search:
            params["search"] = search
        if media_type:
            params["media_type"] = media_type
        if mime_type:
            params["mime_type"] = mime_type
        if author is not None:
            if isinstance(author, list):
                params["author"] = ",".join(map(str, author))
            else:
                params["author"] = author
        if author_exclude:
            params["author_exclude"] = ",".join(map(str, author_exclude))
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        if parent is not None:
            if isinstance(parent, list):
                params["parent"] = ",".join(map(str, parent))
            else:
                params["parent"] = parent
        if parent_exclude:
            params["parent_exclude"] = ",".join(map(str, parent_exclude))
        if status:
            params["status"] = status
        if slug:
            if isinstance(slug, list):
                params["slug"] = ",".join(slug)
            else:
                params["slug"] = slug

        params.update(kwargs)
        response = self._get(self._path, params=params)
        return [Media.model_validate(item) for item in response]

    def upload(
        self,
        file: str | Path | BinaryIO,
        filename: str | None = None,
        title: str | None = None,
        caption: str | None = None,
        alt_text: str | None = None,
        description: str | None = None,
        post: int | None = None,
        **kwargs: Any,
    ) -> Media:
        """Upload a media file.
        
        Args:
            file: Path to file, Path object, or file-like object.
            filename: Override filename (required if file is a file-like object).
            title: Title for the media item.
            caption: Caption for the media item.
            alt_text: Alt text for images.
            description: Description of the media item.
            post: ID of the post to attach the media to.
        """
        if isinstance(file, (str, Path)):
            file_path = Path(file)
            filename = filename or file_path.name
            with open(file_path, "rb") as f:
                content = f.read()
        else:
            if not filename:
                raise ValueError("filename required when uploading file-like object")
            content = file.read()

        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"',
        }
        
        data: dict[str, Any] = {}
        if title:
            data["title"] = title
        if caption:
            data["caption"] = caption
        if alt_text:
            data["alt_text"] = alt_text
        if description:
            data["description"] = description
        if post:
            data["post"] = post
        data.update(kwargs)

        response = self._client._request(
            "POST",
            self._path,
            content=content,
            headers=headers,
            params=data if data else None,
        )
        return Media.model_validate(response)

    def update(self, id: int, data: MediaUpdate | dict[str, Any]) -> Media:
        """Update an existing media item."""
        return super().update(id, data)

    def list_by_type(self, media_type: str, **kwargs: Any) -> list[Media]:
        """List media items by type (image, video, audio, etc.)."""
        return self.list(media_type=media_type, **kwargs)

    def list_images(self, **kwargs: Any) -> list[Media]:
        """List only image files."""
        return self.list_by_type("image", **kwargs)

    def list_videos(self, **kwargs: Any) -> list[Media]:
        """List only video files."""
        return self.list_by_type("video", **kwargs)

    def list_audio(self, **kwargs: Any) -> list[Media]:
        """List only audio files."""
        return self.list_by_type("audio", **kwargs)

    def get_sizes(self, id: int) -> dict[str, Any]:
        """Get available sizes for an image."""
        media = self.get(id)
        if media.media_details and media.media_details.sizes:
            return {k: v.model_dump() for k, v in media.media_details.sizes.items()}
        return {}
