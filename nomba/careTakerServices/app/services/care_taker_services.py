from nomba.careTakerServices.app.models.care_taker import CareTaker
from nomba.careTakerServices.app.repository.care_taker_repo import CareTakerRepo
from nomba.careTakerServices.app.exception.careTakerNotFoundError import CareTakerNotFoundError
from nomba.tenantServices.app.utils.security import hash_password, verify_password


class CareTakerService:
    def __init__(self, repo: CareTakerRepo):
        self.repo = repo

    async def get_my_profile(self, care_taker_id: str) -> CareTaker:
        care_taker = await self.repo.get_care_taker_by_id(care_taker_id)
        if not care_taker:
            raise CareTakerNotFoundError(care_taker_id)
        return care_taker

    async def set_password(self, identifier: str, new_password: str) -> bool:
        care_taker = await self.repo.get_care_taker_by_identifier(identifier)
        if not care_taker:
            raise CareTakerNotFoundError(identifier)
        hashed = hash_password(new_password)
        return await self.repo.update_password(identifier, hashed)

    async def login(self, identifier: str, password: str):
        care_taker = await self.repo.get_care_taker_by_identifier(identifier)
        if not care_taker:
            return None
        stored_password = care_taker.get("password")
        if not stored_password:
            return None
        if not verify_password(password, stored_password):
            return None
        return care_taker
