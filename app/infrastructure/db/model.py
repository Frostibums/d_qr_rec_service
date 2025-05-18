import uuid
from datetime import datetime

from sqlalchemy import UUID, DateTime, LargeBinary, func
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.qr_code import QRCode
from app.infrastructure.db.session import Base


class QRCodeORM(Base):
    __tablename__ = "qr_codes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        index=True,
    )
    qr_data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def to_domain(self) -> QRCode:
        return QRCode(
            id=self.id,
            user_id=self.user_id,
            qr_data=self.qr_data,
            created_at=self.created_at,
        )

    @classmethod
    def from_domain(cls, attendance: QRCode) -> "QRCodeORM":
        return cls(
            id=attendance.id,
            user_id=attendance.user_id,
            qr_data=attendance.qr_data,
            created_at=attendance.created_at,
        )
