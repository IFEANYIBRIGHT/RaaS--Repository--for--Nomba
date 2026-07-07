from nomba.landLordService.app.nomba_client.nomba_client import NombaClient
from nomba.landLordService.app.repository.payment_repo import PaymentRepo
from nomba.landLordService.app.repository.tenant_repo import TenantsRepo


class PaymentService:
    def __init__(
        self,
        nomba_client: NombaClient,
        payment_repo: PaymentRepo,
        tenants_repo: TenantsRepo,
    ):
        self.nomba_client = nomba_client
        self.payment_repo = payment_repo
        self.tenants_repo = tenants_repo

    async def handle_webhook_event(self, payload: dict) -> None:
        data = payload.get("data", {})
        reference = data.get("reference")
        amount = data.get("amount")

        await self.payment_repo.create_payment({
            "reference": reference,
            "amount": amount,
            "status": "successful",
        })
