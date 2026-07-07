import httpx
import os

NOMBA_BASE_URL = os.getenv("NOMBA_BASE_URL", "https://sandbox.nomba.com")
NOMBA_ACCOUNT_ID = os.getenv("NOMBA_ACCOUNT_ID")
NOMBA_CLIENT_ID = os.getenv("NOMBA_CLIENT_ID")
NOMBA_PRIVATE_KEY = os.getenv("NOMBA_PRIVATE_KEY")


class NombaClient:
    def __init__(self):
        self._token: str | None = None

    async def _get_token(self) -> str:
        if self._token:
            return self._token

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{NOMBA_BASE_URL}/v1/auth/token/issue",
                headers={"accountId": NOMBA_ACCOUNT_ID},
                json={
                    "client_id": NOMBA_CLIENT_ID,
                    "private_key": NOMBA_PRIVATE_KEY,
                    "grant_type": "client_credentials",
                },
            )
            response.raise_for_status()
            self._token = response.json()["access_token"]
            return self._token

    async def create_virtual_account(self, tenant_id: str, subaccount_id: str) -> dict:
        token = await self._get_token()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{NOMBA_BASE_URL}/v1/accounts/virtual",
                headers={
                    "Authorization": f"Bearer {token}",
                    "accountId": NOMBA_ACCOUNT_ID,
                },
                json={"subaccountId": subaccount_id, "reference": tenant_id},
            )
            response.raise_for_status()
            return response.json()