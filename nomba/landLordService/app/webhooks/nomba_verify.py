import hmac
import hashlib
import os

NOMBA_PRIVATE_KEY = os.getenv("NOMBA_PRIVATE_KEY")


def verify_signature(raw_body: bytes, signature: str | None) -> bool:
    if not signature or not NOMBA_PRIVATE_KEY:
        return False
    computed = hmac.new(
        NOMBA_PRIVATE_KEY.encode(),
        raw_body,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(computed, signature)
