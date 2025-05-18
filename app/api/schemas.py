from uuid import UUID

from pydantic import BaseModel


class QRCodeOut(BaseModel):
    user_id: UUID
    qr_data: str


class RecognizeInput(BaseModel):
    user_id: UUID
    event_id: UUID
