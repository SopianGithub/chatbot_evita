from starlette.requests import Request
from starlette.responses import JSONResponse

from app import response
from app.models.employe import Employe, Loker
from app.models.lokeremp import Lokeremp
from app.transformers import EmpTransformer

class EmpController:
    @staticmethod
    async def index(request: Request) -> JSONResponse:
        try:
            emp = Employe.objects()
            transformer = EmpTransformer.transform(emp)
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
                lokerinp = listbody['loker']

                loker = Loker()

                loker.bp = lokerinp['bp']
                loker.title = lokerinp['title']
                loker.divisi = lokerinp['divisi']
                loker.unit = lokerinp['unit']
                loker.sub_unit = lokerinp['sub_unit']
                loker.alias = lokerinp['alias']
                loker.save()

                emp = Employe()

                emp.nik = nik
                emp.name = name
                emp.mobile = mobile
                emp.loker = loker

                emp.save()
                transformer = EmpTransformer.singleTransform(emp)

            return response.ok(transformer, "Berhasil Membuat Corporate Customer!")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def show(nik) -> JSONResponse:
        try:
            emp = Employe.objects(nik=nik).first()

            if emp is None:
                raise Exception('PIC tidak ditemukan!')

            transformer = EmpTransformer.singleTransformEdit(emp)
            return response.ok(transformer, "")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def update(nik: int, request: Request) -> JSONResponse:
        try:
            body = await request.json()
            name = body['name']
            mobile = body['mobile']
            lokerinp = body['loker']

            if name == "":
                raise Exception("name couldn't be empty!")

            emp = Employe.objects(nik=nik).first()

            if emp is None:
                raise Exception('PIC tidak ditemukan!')

            loker = Loker.objects(id=emp.loker.id).first()

            loker.bp = lokerinp['bp']
            loker.title = lokerinp['title']
            loker.divisi = lokerinp['divisi']
            loker.unit = lokerinp['unit']
            loker.sub_unit = lokerinp['sub_unit']
            loker.alias = lokerinp['alias']
            loker.save()

            emp.name = name
            emp.mobile = mobile
            emp.loker = loker
            emp.save()

            transformer = EmpTransformer.singleTransform(emp)
            return response.ok(transformer, "Berhasil Mengubah PIC!")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def delete(nik: str) -> JSONResponse:
        try:

            emp = Employe.objects(nik=nik).first()

            if emp is None:
                raise Exception('Employee tidak ditemukan!')

            emp.delete()
            return response.ok('', "Berhasil Menghapus PIC!")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def page(limit: int, offset: int, filterStr = None) -> JSONResponse:
        try:
            if filterStr != None :
                emp = Employe.objects(name__icontains = filterStr).skip(offset).limit(limit)
                lenofemp = Employe.objects(name__icontains = filterStr).count()
            else :
                emp = Employe.objects().skip(offset).limit(limit)
                lenofemp = Employe.objects().count()

            transformer = EmpTransformer.transform(emp)
            result = {'data': transformer, 'total_pages': lenofemp}
            return response.ok(result, "")

        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def showLoker() -> JSONResponse:
        try:
            loker = Lokeremp.objects()

            if loker is None:
                raise Exception('Employee tidak ditemukan!')

            loker_arr = []
            for item in loker:
                tmp_arr = {}
                tmp_arr['id'] = item['divisi']
                tmp_arr['label'] = item['divisi']
                arrch1 = []
                tmp_par = []
                if item['divisi'] != 'DIREKTORAT ENTERPRISE & BUSINESS SERVICE':
                    for ch1 in item['level']:
                        tmp_arrch1 = {}
                        tmp_arrch1['id'] = item['divisi']+"||"+ch1
                        tmp_arrch1['label'] = ch1
                        arrch1.append(tmp_arrch1)
                        arrch2 = []
                        for child2 in item['level'][ch1]:
                            tmp_arrch2 = {}
                            tmp_arrch2['id'] = tmp_arrch1['id']+"||"+child2
                            tmp_arrch2['label'] = child2
                            arrch2.append(tmp_arrch2)
                            arrch3 = []
                            if isinstance(item['level'][ch1][child2], list):
                                for child3 in item['level'][ch1][child2]:
                                    tmp_arrch3 = {}
                                    tmp_arrch3['id'] = tmp_arrch2['id']+"||"+child3
                                    tmp_arrch3['label'] = child3
                                    arrch3.append(tmp_arrch3)

                                tmp_arrch2['children'] = arrch3

                        tmp_par = arrch2

                    tmp_arr['children'] = tmp_par

                loker_arr.append(tmp_arr)

            return response.ok(loker_arr, "")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def deleteSample() -> JSONResponse:
        try:

            emp = Employe.objects(name=None).first()

            if emp is None:
                raise Exception('Corporate Customer tidak ditemukan!')

            emp.delete()
            return response.ok('Ok', "Berhasil Menghapus Corporate Customer!")
        except Exception as e:
            return response.badRequest('', f'{e}')