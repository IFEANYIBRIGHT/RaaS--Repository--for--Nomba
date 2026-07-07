from fastapi import Depends, HTTPException, Request
from fastapi import Request
from app.router.land_lord_router import router
from app.dependencies import get_payment_service
from app.services.payment_services import PaymentService
from app.webhooks.nomba_verify import verify_signature


@router.post("/webhooks/nomba")
async def nomba_webhook(
    request: Request,
    service: PaymentService = Depends(get_payment_service),
):
    raw_body = await request.body()
    signature = request.headers.get("X-Nomba-Signature")

    if not verify_signature(raw_body, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")

    payload = await request.json()
    await service.handle_webhook_event(payload)
    return {"status": "received"}
