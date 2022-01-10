from fastapi import APIRouter
from starlette.requests import Request

from app.controllers.ProductController import ProductController as controller


router = APIRouter()

@router.get("", tags=["product"])
async def action(request: Request):
    return await controller.index(request)

@router.get("/page", tags=["product"])
async def action(limit: int, offset: int, filter = None):
    return await controller.page(limit, offset, filter)


@router.get("/{id}", tags=["product"])
async def action(id: str):
    return await controller.show(id)


@router.post("", tags=["product"])
async def action(request: Request):
    return await controller.store(request)


@router.put("/{id}", tags=["product"])
async def action(id: str, request: Request):
    return await controller.update(id, request)


@router.delete("/{id}", tags=["product"])
async def action(id: str):
    return await controller.delete(id)