import pytest
from httpx import AsyncClient


class TestRedirect:
    @pytest.mark.parametrize("short_id", ("123bad-link", "-=e3321e--_", "1242353402103214030254"))
    async def test_bad_short_id(self, client: AsyncClient, short_id: str):
        response = await client.get(f"/{short_id}")
        assert response.status_code == 404
        assert response.json() == {"detail": "This short link doesn't exist"}
