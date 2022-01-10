from starlette.requests import Request
from starlette.responses import JSONResponse
# from mongoengine import Q

from app import response
from app.models.cc import Cc, SegmenCC
from app.models.am import Am
from app.transformers import CcTransformer

import json

class CcController:

    @staticmethod
    async def index(request: Request) -> JSONResponse:
        try:
            cc = Cc.objects()
            transformer = CcTransformer.transform(cc)
            return response.ok(transformer, "")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def store(request: Request) -> JSONResponse:
        try:
            body = await request.json()
            for listbody in body:
                id_cc = int(listbody['id_cc'])
                name = listbody['name']
                segmeninp = listbody['segmen']
                alias = listbody['alias']

                segmencc = SegmenCC()
                segmencc.id_segmen = segmeninp['id_segmen']
                segmencc.name = segmeninp['name']
                segmencc.descr = segmeninp['descr']

                cc = Cc()

                cc.id_cc = id_cc
                cc.name = name
                cc.segmen = segmencc
                cc.alias = alias
                cc.save()
                transformer = CcTransformer.singleTransform(cc)

            return response.ok(transformer, "Berhasil Membuat Corporate Customer!")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def show(filter) -> JSONResponse:
        try:
            # cc = Cc.objects.filter( (Q(id_cc__icontains=filter) | Q(name__icontains=filter)) | Q(alias__icontains=filter) )
            cc = Cc.objects(id_cc=filter)

            if cc is None:
                raise Exception('Corporate Customer tidak ditemukan!')

            transformer = CcTransformer.transformEdit(cc)
            return response.ok(transformer, "")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def update(id: str, request: Request) -> JSONResponse:
        try:
            body = await request.json()
            name = body['name']
            segmeninp = body['segmen']
            alias = body['alias']

            if name == "":
                raise Exception("name couldn't be empty!")

            cc = Cc.objects(id_cc=id).first()

            if cc is None:
                raise Exception('Corporate Customer tidak ditemukan!')

            segmencc = SegmenCC()
            segmencc.id_segmen = dict(segmeninp)['id_segmen']
            segmencc.name = dict(segmeninp)['name']
            segmencc.descr = dict(segmeninp)['descr']

            cc.name = name
            cc.segmen = segmencc
            cc.alias = alias
            cc.save()

            transformer = CcTransformer.singleTransform(cc)
            return response.ok(transformer, "Berhasil Mengubah Corporate Customer!")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def delete(id: str) -> JSONResponse:
        try:

            cc = Cc.objects(id_cc=id).first()

            if cc is None:
                raise Exception('Corporate Customer tidak ditemukan!')

            cc.delete()
            return response.ok('', "Berhasil Menghapus Corporate Customer!")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def page(limit: int, offset: int, filterStr = None) -> JSONResponse:
        try:
            if filterStr != None :
                cc = Cc.objects(name__icontains = filterStr).skip(offset).limit(limit)
                lenofcc = Cc.objects(name__icontains = filterStr).count()
            else :
                cc = Cc.objects().skip(offset).limit(limit)
                lenofcc = Cc.objects().count()

            transformer = CcTransformer.transform(cc)
            result = {'data': transformer, 'total_pages': lenofcc}
            return response.ok(result, "")

        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def mapping(id: str, request: Request) -> JSONResponse:
        try:
            body = await request.json()
            cc = Cc.objects(id_cc=id).first()

            if cc is None:
                raise Exception('Corporate Customer tidak ditemukan!')

            listam = []
            for listbody in body:
                am = Am()
                am.nik = listbody['nik']
                am.name = listbody['name']
                am.mobile = listbody['mobile']
                listam.append(am)

            cc.mapping_am = listam
            cc.save()

            transformer = CcTransformer.singleTransform(cc)
            return response.ok(transformer, "Berhasil Mengubah Corporate Customer!")
        except Exception as e:
            return response.badRequest('', f'{e}')


    async def showMapping(filter) -> JSONResponse:
        try:
            cc = Cc.objects(id_cc=filter)

            if cc is None:
                raise Exception('Corporate Customer tidak ditemukan!')

            transformer = CcTransformer.transformmap(cc)
            return response.ok(transformer, "")
        except Exception as e:
            return response.badRequest('', f'{e}')