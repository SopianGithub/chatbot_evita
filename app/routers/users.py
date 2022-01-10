from fastapi import APIRouter
from starlette.requests import Request

from app.controllers.UserController import UserController as controller

router = APIRouter()

@router.get("/test")
async def action():
    return {"message": "Hello World"}

@router.get("", tags=["userss"])
async def read_users():
    return [{"username": "Foo"}, {"username": "Bar"}]

@router.get("", tags=["users"])
async def action(request: Request):
    return await controller.index(request)


@router.get("/{id}", tags=["users"])
async def action(id: str):
    return await controller.show(id)


@router.post("", tags=["users"])
async def action(request: Request):
    return await controller.store(request)


@router.put("/{id}", tags=["users"])
async def action(id: str, request: Request):
    return await controller.update(id, request)


@router.delete("/{id}", tags=["users"])
async def action(id: str):
    return await controller.delete(id)