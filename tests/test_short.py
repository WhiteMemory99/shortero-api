import pytest
from httpx import AsyncClient


class TestShorteningEndpoints:
    @pytest.mark.parametrize(
        "url",
        (
            "eergerg211",
            "htt://somarfd.tx",
            "14334215236",
            "ls4fde",
            "xyz.co",
            "https://dewfwe",
            "http://dsdw",
            "https:/1231244",
        ),
    )
    async def test_bad_urls(self, client: AsyncClient, url: str):
        response = await client.post("/api/shorten", params={"url": url})
        assert response.status_code == 422

    @pytest.mark.parametrize("url", ("https://example.com", "http://example.com"))
    async def test_good_urls(self, client: AsyncClient, url: str):
        response = await client.post("/api/shorten", params={"url": url})
        assert response.status_code == 201
        assert response.text is not None
