from fastapi import APIRouter
from starlette.requests import Request

from app.controllers.AmControlles import AmController as controller


router = APIRouter()

@router.get("", tags=["ams"])
async def action(request: Request):
    return await controller.index(request)

@router.get("/page", tags=["ams"])
async def action(limit: int, offset: int, filter = None):
    return await controller.page(limit, offset, filter)

@router.get("/search/{prm}", tags=["ams"])
async def action(prm: str):
    return await controller.searchAM(prm)

@router.get("/{id}", tags=["ams"])
async def action(id: str):
    return await controller.show(id)

@router.post("", tags=["ams"])
async def action(request: Request):
    return await controller.store(request)


@router.put("/{id}", tags=["ams"])
async def action(id: str, request: Request):
    return await controller.update(id, request)


@router.delete("/{id}", tags=["ams"])
async def action(id: str):
    return await controller.delete(id)