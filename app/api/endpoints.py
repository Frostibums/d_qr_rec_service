from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.api.dependencies import (
    get_current_teacher_id,
    get_current_user_id,
    get_producer,
    get_qr_service,
)
from app.api.schemas import QRCodeOut, RecognizeInput
from app.infrastructure.bus.kafka.producer import KafkaEventProducer
from app.service.qr import QRCodeService

router = APIRouter(prefix="/qr", tags=["QR Code"])


@router.get(
    "/healthcheck",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
async def healthcheck():
    return {
        'status': 'ok',
    }


@router.post(
    "/recognize",
    status_code=status.HTTP_202_ACCEPTED,
)
async def recognize_qr(
        payload: RecognizeInput,
        producer: KafkaEventProducer = Depends(get_producer),
        teacher_id: UUID = Depends(get_current_teacher_id)
):
    await producer.send(
        "student-recognized",
        {
            "event_id": str(payload.event_id),
            "student_id": str(payload.user_id),
            "teacher_id": str(teacher_id),
        }
    )


@router.get("/", response_model=QRCodeOut)
async def get_qr_code(
        user_id: UUID = Depends(get_current_user_id),
        service: QRCodeService = Depends(get_qr_service),
):
    qr = await service.get_qr_code(user_id)
    if not qr:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="QR code not found",
        )
    return qr
