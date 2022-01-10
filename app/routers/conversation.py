from fastapi import APIRouter
from starlette.requests import Request

from app.controllers.Conversation import Conversation as controller

router = APIRouter()

@router.post("", tags=["hook"])
async def action(request: Request):
    return await controller.index(request)