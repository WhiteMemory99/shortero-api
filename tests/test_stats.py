import pytest
from httpx import AsyncClient


class TestStatsEndpoints:
    test_url = "https://example.com"

    @pytest.mark.parametrize(
        "url",
        (
            "https://google.com",
            "https://yandex.ru",
        ),
    )
    async def test_non_existing_urls(self, client: AsyncClient, url: str):
        response = await client.post("/api/stats", params={"url": url})
        assert response.status_code == 404
        assert response.json() == {"detail": "This URL doesn't have a short link"}

    async def test_existing_urls(self, client: AsyncClient):
        response = await client.post("/api/shorten", params={"url": self.test_url})
        assert response.status_code == 201

        response = await client.post("/api/stats", params={"url": self.test_url})
        assert response.status_code == 200
        assert response.json() == {"original_url": self.test_url, "clicks": 0}

    async def test_clicks_increment(self, client: AsyncClient):
        response = await client.post("/api/shorten", params={"url": self.test_url})
        assert response.status_code == 201

        short_id = response.text.rsplit("/", maxsplit=1)[-1]
        response = await client.get(f"/{short_id}")
        assert response.status_code == 307

        response = await client.post("/api/stats", params={"url": self.test_url})
        assert response.status_code == 200
        assert response.json()["clicks"] == 1
