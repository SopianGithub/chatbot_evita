from fastapi import APIRouter
from starlette.requests import Request

from app.controllers.CcController import CcController as controller

router = APIRouter()

@router.get("", tags=["cc"])
async def action(request: Request):
    return await controller.index(request)

@router.get("/page", tags=["cc"])
async def action(limit: int, offset: int, filter = None):
    return await controller.page(limit, offset, filter)


@router.get("/{id}", tags=["cc"])
async def action(id: str):
    return await controller.show(id)

@router.get("/mapping/{id}", tags=["cc"])
async def action(id: str, request: Request):
    return await controller.showMapping(id)

@router.post("", tags=["cc"])
async def action(request: Request):
    return await controller.store(request)


@router.put("/{id}", tags=["cc"])
async def action(id: str, request: Request):
    return await controller.update(id, request)

@router.put("/mapping/{id}", tags=["cc"])
async def action(id: str, request: Request):
    return await controller.mapping(id, request)

@router.delete("/{id}", tags=["cc"])
async def action(id: str):
    return await controller.delete(id)