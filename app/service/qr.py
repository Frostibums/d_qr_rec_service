from io import BytesIO
from uuid import UUID

import qrcode

from app.domain.qr_code import QRCode
from app.infrastructure.db.repo import QRCodeRepository


class QRCodeService:
    def __init__(self, repository: QRCodeRepository):
        self.repository = repository

    async def create_qr_code(self, user_id: UUID, qr_data: str) -> QRCode:
        qr = qrcode.QRCode(box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        buffer = BytesIO()
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(buffer, format="PNG")

        old_qr = await self.repository.get_by_user_id(user_id)
        if old_qr is not None:
            return await self.repository.update(user_id, buffer.getvalue())
        return await self.repository.create(user_id, buffer.getvalue())

    async def get_qr_code(self, user_id: UUID) -> QRCode | None:
        return await self.repository.get_by_user_id(user_id)
