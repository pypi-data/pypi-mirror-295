from unittest.mock import AsyncMock, patch

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
    pass


def test_sync_save_images(sync_generator):
    pass


@pytest.mark.asyncio
async def test_async_generate_images(async_generator):
    with patch("Bing.bing.aiohttp.ClientSession.post", new=AsyncMock()) as mock_post:
        pass

    with patch("Bing.bing.aiohttp.ClientSession.get", new=AsyncMock()) as mock_get:
        pass


@pytest.mark.asyncio
async def test_async_save_images(async_generator):
    with patch("Bing.bing.aiofiles.open", new=AsyncMock()) as mock_open:
        pass
