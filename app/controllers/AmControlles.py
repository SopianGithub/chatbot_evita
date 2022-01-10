from starlette.requests import Request
from starlette.responses import JSONResponse
from mongoengine.queryset.visitor import Q

from app import response
from app.models.am import Am
from app.transformers import AmTransformer

class AmController:
    @staticmethod
    async def index(request: Request) -> JSONResponse:
        try:
            ams = Am.objects()
            transformer = AmTransformer.transform(ams)
            return response.ok(transformer, "")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def store(request: Request) -> JSONResponse:
        try:
            body = await request.json()
            for listbody in body:
                nik = listbody['nik']
                name = listbody['name']
                mobile = listbody['mobile']

                am = Am()

                am.nik = nik
                am.name = name
                am.mobile = mobile
                am.save()
                transformer = AmTransformer.singleTransform(am)

            return response.ok(transformer, "Berhasil Membuat Account Manager!")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def show(nik) -> JSONResponse:
        try:
            am = Am.objects(nik=str(nik))

            if am is None:
                raise Exception('Account Manager tidak ditemukan!')

            transformer = AmTransformer.transformEdit(am)
            return response.ok(transformer, "")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def update(id: str, request: Request) -> JSONResponse:
        try:
            body = await request.json()
            name = body['name']
            mobile = body['mobile']

            if name == "":
                raise Exception("name couldn't be empty!")

            am = Am.objects(nik=id).first()

            if am is None:
                raise Exception('Account Manager tidak ditemukan!')

            am.name = name
            am.mobile = mobile
            am.save()

            transformer = AmTransformer.singleTransform(am)
            return response.ok(transformer, "Berhasil Mengubah Account Manager!")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def delete(id: str) -> JSONResponse:
        try:

            am = Am.objects(nik=id).first()

            if am is None:
                raise Exception('Account Manager tidak ditemukan!')

            am.delete()
            return response.ok('', "Berhasil Menghapus Account Manager!")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def page(limit: int, offset: int, filterStr = None) -> JSONResponse:
        try:
            if filterStr != None :
                am = Am.objects(name__icontains = filterStr).skip(offset).limit(limit)
                lenofam = Am.objects(name__icontains = filterStr).count()
            else :
                am = Am.objects().skip(offset).limit(limit)
                lenofam = Am.objects().count()

            transformer = AmTransformer.transform(am)
            result = {'data': transformer, 'total_pages': lenofam}
            return response.ok(result, "")

        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def searchAM(prm) -> JSONResponse:
        try:
            am = Am.objects((Q(nik__icontains=str(prm))) | (Q(name__icontains=prm)))

            if am is None:
                raise Exception('Account Manager tidak ditemukan!')

            transformer = AmTransformer.transformMapping(am)
            return response.ok(transformer, "")
        except Exception as e:
            return response.badRequest('', f'{e}')