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
        event_type = payload.get("event_type")
        if event_type != "payment_success":
            return  # ignore payment_failed, payout_success, etc. for now

        data = payload.get("data", {})
        transaction = data.get("transaction", {})

        reference = transaction.get("merchantTxRef") or transaction.get("transactionId")
        amount = transaction.get("transactionAmount")
        alias_account = transaction.get("aliasAccountNumber")

        await self.payment_repo.create_payment({
            "reference": reference,
            "amount": amount,
            "alias_account_number": alias_account,
            "status": "successful",
        })
