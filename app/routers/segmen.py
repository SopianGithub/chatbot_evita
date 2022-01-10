from fastapi import APIRouter
from starlette.requests import Request

from app.controllers.SegmenController import SegmenController as controller


router = APIRouter()

@router.get("", tags=["segmen"])
async def action(request: Request):
    return await controller.index(request)

@router.get("/{id}", tags=["segmen"])
async def action(id: str):
    return await controller.show(id)


@router.post("", tags=["segmen"])
async def action(request: Request):
    return await controller.store(request)


@router.put("/{id}", tags=["segmen"])
async def action(id: str, request: Request):
    return await controller.update(id, request)


@router.delete("/{id}", tags=["segmen"])
async def action(id: str):
    return await controller.delete(id)