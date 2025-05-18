from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from app.domain.role_enum import Role
from app.infrastructure.bus.kafka.producer import KafkaEventProducer
from app.infrastructure.db.repo import QRCodeRepository
from app.infrastructure.db.session import get_session
from app.infrastructure.security import decode_jwt_token
from app.service.qr import QRCodeService


def get_jwt_payload(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing access token",
        )

    if token.startswith("Bearer "):
        token = token[7:]
    try:
        return decode_jwt_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


def get_current_teacher_id(payload: dict = Depends(get_jwt_payload)) -> UUID:
    if payload.get("role") not in (Role.teacher, Role.admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only for stuff"
        )
    return UUID(payload["sub"])


def get_current_user_id(payload: dict = Depends(get_jwt_payload)) -> UUID:
    return UUID(payload["sub"])


def get_producer(request: Request) -> KafkaEventProducer:
    return request.app.state.kafka_producer


def get_repo(session: AsyncSession = Depends(get_session)) -> QRCodeRepository:
    return QRCodeRepository(session)


def get_qr_service(repo: QRCodeRepository = Depends(get_repo)) -> QRCodeService:
    return QRCodeService(repo)
