from fastapi import APIRouter
from starlette.requests import Request

from app.controllers.Report import Report as controller

router = APIRouter()

@router.get("/category", tags=["Report"])
async def action(request: Request):
    return await controller.index(request)

@router.get("/product", tags=["Report"])
async def action(request: Request):
    return await controller.product(request)

@router.get("/answered", tags=["Report"])
async def action(request: Request):
    return await controller.answered(request)

@router.get("/page_catgeory", tags=["Report"])
async def action(limit: int, offset: int):
    return await controller.pageCategory(limit, offset)

@router.get("/page_chart_product", tags=["Report"])
async def action(limit: int, offset: int):
    return await controller.pageProduct(limit, offset)

@router.get("/page_answered", tags=["Report"])
async def action(limit: int, offset: int):
    return await controller.pageAnswerd(limit, offset)

@router.get("/searching", tags=["Report"])
async def action(search: str, category: str):
    return await controller.searchMapp(search, category)

@router.post("/update_logs/{id}", tags=["Report"])
async def action(id: str, request: Request):
    return await controller.updateMapLog(id, request)

@router.post("/update_pic", tags=["Report"])
async def action(request: Request):
    return await controller.updateAliasPIC(request)

@router.post("/update_product", tags=["Report"])
async def action(request: Request):
    return await controller.updateAliasProduct(request)

@router.post("/update_customer", tags=["Report"])
async def action(request: Request):
    return await controller.updateAliasCustomer(request)