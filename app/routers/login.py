from fastapi import APIRouter
from starlette.requests import Request

from app.controllers.LoginController import LoginController as controller

router = APIRouter()

@router.post("", tags=["login"])
async def action(request: Request):
    return await controller.login(request)

@router.get("/{id}", tags=["login"])
async def action(id: str):
    return await controller.show(id)

@router.post("/create", tags=["login"])
async def action(request: Request):
    return await controller.createUser(request)