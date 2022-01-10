from fastapi import APIRouter
from starlette.requests import Request

from app.controllers.EmpController import EmpController as controller


router = APIRouter()

@router.get("", tags=["employe"])
async def action(request: Request):
    return await controller.index(request)

@router.get("/page", tags=["employe"])
async def action(limit: int, offset: int, filter = None):
    return await controller.page(limit, offset, filter)

@router.get("/loker", tags=["employe"])
async def action():
    return await controller.showLoker()

@router.get("/sample", tags=["employe"])
async def action():
    return await controller.deleteSample()

@router.get("/{nik}", tags=["employe"])
async def action(nik: str):
    return await controller.show(nik)

@router.post("", tags=["employe"])
async def action(request: Request):
    return await controller.store(request)


@router.put("/{nik}", tags=["employe"])
async def action(nik: int, request: Request):
    return await controller.update(nik, request)


@router.delete("/{id}", tags=["employe"])
async def action(id: str):
    return await controller.delete(id)
