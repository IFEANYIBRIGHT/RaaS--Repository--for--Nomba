from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

from nomba.landLordService.app.nomba_client.nomba_client import NombaClient


class TestNombaClient(IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = NombaClient()

    @patch("nomba.landLordService.app.nomba_client.nomba_client.httpx.AsyncClient")
    async def test_get_token_returns_access_token(self, mock_async_client):
        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": "fake-token-123"}
        mock_response.raise_for_status = lambda: None

        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance

        token = await self.client._get_token()

        self.assertEqual(token, "fake-token-123")
        mock_client_instance.post.assert_called_once()

    @patch("nomba.landLordService.app.nomba_client.nomba_client.httpx.AsyncClient")
    async def test_get_token_caches_after_first_call(self, mock_async_client):
        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": "cached-token"}
        mock_response.raise_for_status = lambda: None

        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance

        await self.client._get_token()
        await self.client._get_token()

        mock_client_instance.post.assert_called_once()

    @patch("nomba.landLordService.app.nomba_client.nomba_client.httpx.AsyncClient")
    async def test_create_virtual_account_returns_response_data(self, mock_async_client):
        self.client._token = "fake-token"

        mock_response = MagicMock()
        mock_response.json.return_value = {"accountNumber": "9038421765"}
        mock_response.raise_for_status = lambda: None

        mock_client_instance = AsyncMock()
        mock_client_instance.post.return_value = mock_response
        mock_async_client.return_value.__aenter__.return_value = mock_client_instance

        result = await self.client.create_virtual_account("tenant123", "subacc456")

        self.assertEqual(result["accountNumber"], "9038421765")