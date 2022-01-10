from fastapi import APIRouter
from starlette.requests import Request

from app.controllers.ChatController import ChatController as controller

router = APIRouter()

@router.post("", tags=["webhook"])
async def action(request: Request):
    return await controller.webhook(request)