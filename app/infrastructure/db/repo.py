from datetime import datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.qr_code import QRCode
from app.infrastructure.db.model import QRCodeORM


class QRCodeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: UUID, qr_data: bytes) -> QRCode:
        qr_db = QRCodeORM(user_id=user_id, qr_data=qr_data)
        qr_db.qr_data = qr_data
        self.session.add(qr_db)
        await self.session.commit()
        await self.session.refresh(qr_db)
        return qr_db.to_domain()

    async def update(self, user_id: UUID, qr_data: bytes) -> QRCode:
        stmt = update(
            QRCodeORM
        ).where(
            QRCodeORM.user_id == user_id
        ).values(
            qr_data=qr_data,
            created_at=datetime.utcnow(),
        )
        await self.session.execute(stmt)
        await self.session.commit()
        return await self.get_by_user_id(user_id)

    async def get_by_user_id(self, user_id: UUID) -> QRCode | None:
        stmt = select(QRCodeORM).where(QRCodeORM.user_id == user_id)
        result = await self.session.execute(stmt)
        qr_db = result.scalar_one_or_none()
        return qr_db.to_domain() if qr_db else None
