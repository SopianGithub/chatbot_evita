from starlette.requests import Request
from starlette.responses import JSONResponse

from app import response
from app.models.segmen import Segmen
from app.transformers import SegmenTransform

class SegmenController:
    @staticmethod
    async def index(request: Request) -> JSONResponse:
        try:
            segmen = Segmen.objects()
            transformer = SegmenTransform.transform(segmen)
            return response.ok(transformer, "")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def store(request: Request) -> JSONResponse:
        try:
            body = await request.json()
            for listbody in body:
                id_segmen = listbody['id_segmen']
                name = listbody['name']
                descr = listbody['descr']

                segmen = Segmen()

                segmen.id_segmen = id_segmen
                segmen.name = name
                segmen.descr = descr
                segmen.save()
                transformer = SegmenTransform.singleTransform(segmen)

            return response.ok(transformer, "Berhasil Membuat Segmen!")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def show(id) -> JSONResponse:
        try:
            am = Segmen.objects(id_segmen=id).first()

            if am is None:
                raise Exception('Segmen tidak ditemukan!')

            transformer = SegmenTransform.singleTransform(am)
            return response.ok(transformer, "")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def update(id: str, request: Request) -> JSONResponse:
        try:
            body = await request.json()
            name = body['name']
            desc = body['descr']

            if name == "":
                raise Exception("name couldn't be empty!")

            segmen = Segmen.objects(id_segmen=id).first()

            if segmen is None:
                raise Exception('Segmen tidak ditemukan!')

            segmen.name = name
            segmen.descr = desc
            segmen.save()

            transformer = SegmenTransform.singleTransform(segmen)
            return response.ok(transformer, "Berhasil Mengubah Segmen!")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def delete(id: str) -> JSONResponse:
        try:

            segmen = Segmen.objects(id_segmen=id).first()

            if segmen is None:
                raise Exception('Segmen tidak ditemukan!')

            segmen.delete()
            return response.ok('', "Berhasil Menghapus Segmen!")
        except Exception as e:
            return response.badRequest('', f'{e}')