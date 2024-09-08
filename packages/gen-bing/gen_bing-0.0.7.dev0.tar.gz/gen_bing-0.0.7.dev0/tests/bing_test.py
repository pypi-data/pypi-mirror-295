from unittest.mock import AsyncMock, Mock, patch

import pytest

from Bing.bing import AsyncImageGenerator, ImageGenerator


@pytest.fixture
def sync_generator():
    return ImageGenerator(
        auth_cookie_u="test_u", auth_cookie_srchhpgusr="test_srchhpgusr"
    )


@pytest.fixture
def async_generator():
    return AsyncImageGenerator(
        auth_cookie_u="test_u", auth_cookie_srchhpgusr="test_srchhpgusr"
    )


def test_sync_generate_images(sync_generator):
    with patch("requests.Session.post", new=Mock()) as mock_post:
        mock_post.return_value.status_code = 302
        mock_post.return_value.headers = {"Location": "https://bing.com/some_id"}
        mock_post.return_value.text = '<img src="https://tse.some_image?w=600">'

        with patch("requests.Session.get", new=Mock()) as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = '<img src="https://tse.some_image?w=600">'

            images = sync_generator.generate("test prompt", 1)

            assert len(images) == 1
            assert images[0] == "https://tse.some_image"


def test_sync_save_images(sync_generator):
    with patch("requests.Session.get", new=Mock()) as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"image data"

        with patch("builtins.open", new=Mock()) as mock_open:
            sync_generator.save(["https://tse.some_image"], "test_dir")

            mock_open.assert_called_once_with("test_dir/some_image.jpeg", "wb")
            mock_open().write.assert_called_once_with(b"image data")


@pytest.mark.asyncio
async def test_async_generate_images(async_generator):
    with patch("httpx.AsyncClient.post", new=AsyncMock()) as mock_post:
        mock_post.return_value.status_code = 302
        mock_post.return_value.headers = {"Location": "https://bing.com/some_id"}
        mock_post.return_value.text = '<img src="https://tse.some_image?w=600">'

        with patch("httpx.AsyncClient.get", new=AsyncMock()) as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = '<img src="https://tse.some_image?w=600">'

            images = await async_generator.generate("test prompt", 1)

            assert len(images) == 1
            assert images[0] == "https://tse.some_image"


@pytest.mark.asyncio
async def test_async_save_images(async_generator):
    with patch("httpx.AsyncClient.get", new=AsyncMock()) as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"image data"

        with patch("aiofiles.open", new=AsyncMock()) as mock_open:
            await async_generator.save(["https://tse.some_image"], "test_dir")

            mock_open.assert_called_once_with("test_dir/some_image.jpeg", "wb")
            mock_open().write.assert_called_once_with(b"image data")
