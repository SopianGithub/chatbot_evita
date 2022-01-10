from starlette.requests import Request
from starlette.responses import JSONResponse
import json

from app import response
from app.models.product import Product, ProductFiles
from app.transformers import ProductTransformer

class ProductController:
    @staticmethod
    async def index(request: Request) -> JSONResponse:
        try:
            prod = Product.objects()
            transformer = ProductTransformer.transform(prod)
            return response.ok(transformer, "")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def store(request: Request) -> JSONResponse:
        try:
            body = await request.json()
            for listbody in body:
                name = listbody['name']
                desc = listbody['desc']
                benefit = listbody['benefit']
                alias = listbody['alias']
                productfile = listbody['files']

                listFileProd = []
                for listFiles in productfile:
                    file_prod = ProductFiles()
                    file_prod.type_file = listFiles['type_file']
                    file_prod.url_file = listFiles['url_file']
                    listFileProd.append(file_prod)

                prod = Product()

                prod.name = name
                prod.desc = desc
                prod.benefit = benefit
                prod.alias = alias
                prod.productfile = listFileProd

                prod.save()
                transformer = ProductTransformer.singleTransform(prod)

            return response.ok(transformer, "Berhasil Membuat Corporate Customer!")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def show(id) -> JSONResponse:
        try:
            prod = Product.objects(id=id)

            if prod is None:
                raise Exception('Corporate Customer tidak ditemukan!')

            transformer = ProductTransformer.transformEdit(prod)
            return response.ok(transformer, "")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def update(id: str, request: Request) -> JSONResponse:
        try:
            body = await request.json()
            for listbody in body:
                name = listbody['name']
                desc = listbody['desc']
                benefit = listbody['benefit']
                alias = listbody['alias']
                productfile = listbody['files']

                prod = Product.objects(id=id).first()

                if prod is None:
                    raise Exception('Product tidak ditemukan!')

                listFileProd = []
                for listFiles in productfile:
                    file_prod = ProductFiles()
                    file_prod.type_file = listFiles['type_file']
                    file_prod.url_file = listFiles['url_file']
                    listFileProd.append(file_prod)

                prod.name = name
                prod.desc = desc
                prod.benefit = benefit
                prod.alias = alias
                prod.productfile = listFileProd
                prod.save()

                transformer = ProductTransformer.singleTransform(prod)

            return response.ok(transformer, "Berhasil Mengubah Product!")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def delete(id: str) -> JSONResponse:
        try:

            prod = Product.objects(id=id).first()

            if prod is None:
                raise Exception('Corporate Customer tidak ditemukan!')

            prod.delete()
            return response.ok('', "Berhasil Menghapus Corporate Customer!")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def page(limit: int, offset: int, filterStr = None) -> JSONResponse:
        try:
            if filterStr != None :
                emp = Product.objects(name__icontains = filterStr).skip(offset).limit(limit)
                lenofemp = Product.objects(name__icontains = filterStr).count()
            else :
                emp = Product.objects().skip(offset).limit(limit)
                lenofemp = Product.objects().count()

            transformer = ProductTransformer.transform(emp)
            result = {'data': transformer, 'total_pages': lenofemp}
            return response.ok(result, "")

        except Exception as e:
            return response.badRequest('', f'{e}')