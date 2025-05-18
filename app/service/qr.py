from uuid import UUID

from app.domain.qr_code import QRCode
from app.infrastructure.db.repo import QRCodeRepository


class QRCodeService:
    def __init__(self, repository: QRCodeRepository):
        self.repository = repository

    async def create_qr_code(self, user_id: UUID, qr_data: str) -> QRCode:
        old_qr = await self.repository.get_by_user_id(user_id)
        if old_qr is not None:
            return await self.repository.update(user_id, qr_data)
        return await self.repository.create(user_id, qr_data)

    async def get_qr_code(self, user_id: UUID) -> QRCode | None:
        return await self.repository.get_by_user_id(user_id)
