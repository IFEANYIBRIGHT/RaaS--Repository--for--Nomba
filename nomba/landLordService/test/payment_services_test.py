from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from nomba.landLordService.app.services.payment_services import PaymentService


class TestPaymentService(IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_nomba_client = AsyncMock()
        self.mock_payment_repo = AsyncMock()
        self.mock_tenants_repo = AsyncMock()

        self.service = PaymentService(
            nomba_client=self.mock_nomba_client,
            payment_repo=self.mock_payment_repo,
            tenants_repo=self.mock_tenants_repo,
        )

    async def test_handle_webhook_event_creates_payment_record(self):
        payload = {
            "data": {
                "reference": "RAAS-T001-P001",
                "amount": 200000,
            }
        }

        await self.service.handle_webhook_event(payload)

        self.mock_payment_repo.create_payment.assert_called_once_with({
            "reference": "RAAS-T001-P001",
            "amount": 200000,
            "status": "successful",
        })

    async def test_handle_webhook_event_missing_data_does_not_crash(self):
        payload = {"data": {}}

        await self.service.handle_webhook_event(payload)

        self.mock_payment_repo.create_payment.assert_called_once_with({
            "reference": None,
            "amount": None,
            "status": "successful",
        })