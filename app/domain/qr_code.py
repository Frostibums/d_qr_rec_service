from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class QRCode:
    id: UUID
    user_id: UUID
    qr_data: bytes
    created_at: datetime
