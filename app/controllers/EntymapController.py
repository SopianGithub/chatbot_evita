from starlette.requests import Request
from starlette.responses import JSONResponse
# from mongoengine import Q

from app.models.cc import Cc
from app.models.employe import Employe
from app.models.product import Product

class EntymapController:

    @staticmethod
    async def index(filter) -> JSONResponse:
        if filter == "cc":
            data = Cc.objects()
        elif filter == "pic":
            data = Employe.objects()
        elif filter == "product":
            data = Product.objects()
