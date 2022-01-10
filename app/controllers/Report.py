from starlette.requests import Request
from starlette.responses import JSONResponse
from app import response
import json
import datetime
from mongoengine.queryset.visitor import Q
from collections import Counter

from app.models.logs import Logs
from app.models.product import Product
from app.models.cc import Cc
from app.models.employe import Employe, Loker

class Report:

    @staticmethod
    async def index(request: Request) -> JSONResponse:
        try:
            jum_cus = Logs.objects(Q(intent="customer") | Q(context="customer_page")).count()
            jum_pic = Logs.objects(Q(intent="PICJobs") | Q(context="pic_page")).count()
            jum_product = Logs.objects(Q(intent="Product") | Q(context="product_page")).count()
            jum_am = Logs.objects(Q(intent="AccountMgr") | Q(context="am_page")).count()
            result_report = {
                "Corporate Customer": jum_cus,
                "PIC": jum_pic,
                "Product": jum_product,
                "Account Manager": jum_am,
            }
            return response.ok(result_report, "")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def product(request: Request) -> JSONResponse:
        try:
            product = Logs.objects(Q(intent="Details") & Q(context="product_page"))

            arr_log_id_prod = []
            for item in product:
                name_of_prod = Product.objects(id=item.parameter['idprod'])
                name_product = ""
                for prod in name_of_prod:
                    name_product = prod.name
                arr_log_id_prod.append(name_product)

            countOfProd = Counter(arr_log_id_prod)

            return response.ok(dict(countOfProd), "")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def answered(request: Request) -> JSONResponse:
        try:
            loganswer = Logs.objects(isResponse=True)
            lognotanswer = Logs.objects(isResponse=False)
            arrLogByCat =  []
            arrLogNotAnsw = []
            ContextOfIntent = {'customer_page': 'Corporate Customer', 'am_page':'Account Manager', 'product_page': 'Product', 'pic_page': 'PIC'}
            for item in loganswer:
                if(len(item.parameter) > 0):
                    arrLogByCat.append(ContextOfIntent[item.context])

            countOfAnsw = Counter(arrLogByCat)

            for item in lognotanswer:
                if(len(item.parameter) > 0):
                    arrLogNotAnsw.append(ContextOfIntent[item.context])

            countOfNotAnsw = Counter(arrLogNotAnsw)

            res = {
                "Answered" : dict(countOfAnsw),
                "Not Answered": dict(countOfNotAnsw)
            }

            for key, value in ContextOfIntent.items():
                if res['Not Answered'].get(value) is None:
                    res['Not Answered'][value] = 0

            for key, value in ContextOfIntent.items():
                if res['Answered'].get(value) is None:
                    res['Answered'][value] = 0

            return response.ok(res, "")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def pageCategory(limit: int, offset: int) -> JSONResponse:
        try:
            data_category = Logs.objects(Q(intent="customer") | Q(intent="PICJobs") | Q(intent="Product") | Q(intent="AccountMgr") | Q(context="customer_page")| Q(context="pic_page") | Q(context="am_page") | Q(context="product_page")).skip(offset).limit(limit)
            jum_category = Logs.objects(Q(intent="customer") | Q(intent="PICJobs") | Q(intent="Product") | Q(intent="AccountMgr") | Q(context="customer_page")| Q(context="pic_page") | Q(context="am_page") | Q(context="product_page")).count()

            ret_date = []
            for item in data_category:
                ret_date.append({
                    'intent': item.intent,
                    'context': item.context,
                    'isResponse': item.isResponse,
                    'idTelegram': item.idTelegram.split('.', 1)[0],
                    'potretdate': item.potretdate.astimezone().strftime("%Y-%m-%d %H:%M:%S.%f%z")
                })
            # json.loads(data_category.to_json())
            result = {'data': list(ret_date), 'total_pages': jum_category}
            return response.ok(result, "")

        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def pageProduct(limit: int, offset: int) -> JSONResponse:
        try:
            data_product = Logs.objects(Q(intent="Details") & Q(context="product_page")).skip(offset).limit(limit)
            jum_product = Logs.objects(Q(intent="Details") & Q(context="product_page")).count()

            ret_date = []
            for item in data_product:
                name_of_prod = Product.objects(id=item.parameter['idprod'])
                name_product = ""
                for prod in name_of_prod:
                    name_product = prod.name
                ret_date.append({
                    'intent': item.intent,
                    'context': item.context,
                    'isResponse': item.isResponse,
                    'parameter': name_product,
                    'idTelegram': item.idTelegram.split('.', 1)[0],
                    'potretdate': item.potretdate.astimezone().strftime("%Y-%m-%d %H:%M:%S.%f%z")
                })
            # json.loads(data_category.to_json())
            result = {'data': list(ret_date), 'total_pages': jum_product}
            return response.ok(result, "")

        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def pageAnswerd(limit: int, offset: int) -> JSONResponse:
        try:
            data_amsw = Logs.objects(Q(parameter__exists=True) & Q(parameter__ne={})).skip(offset).limit(limit).order_by('isResponse')
            jum_answ = Logs.objects(Q(parameter__exists=True) & Q(parameter__ne={})).count()

            ret_date = []
            for item in data_amsw:
                ret_date.append({
                    'id': str(item.id),
                    'intent': item.intent,
                    'context': item.context,
                    'isResponse': item.isResponse,
                    'isMapped': item.isMapped,
                    'isPossibleMap': item.isPossibleMap,
                    'parameter': item.parameter,
                    'idTelegram': item.idTelegram.split('.', 1)[0],
                    'potretdate': item.potretdate.astimezone().strftime("%Y-%m-%d %H:%M:%S.%f%z")
                })

            result = {'data': list(ret_date), 'total_pages': jum_answ}
            return response.ok(result, "")

        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def searchMapp(search: str, category: str) -> JSONResponse:
        try:
            if category == "Customer":
                cc = Cc.objects(Q(name__icontains=search))
                arrCustomer = []
                for item in cc:
                    arrCustomer.append({
                        'id': item.id,
                        'name': item.name,
                        'segmen': item.segmen.name
                    })
                objCC = {
                    "category": category,
                    "items": list(arrCustomer)
                }
                return response.ok(objCC, "Success")
            elif category == "Product":
                product = Product.objects(Q(name__icontains=search) | Q(desc__icontains=search))
                arrProduct = []
                for item in product:
                    arrProduct.append({
                        'id': str(item.id),
                        'name': item.name,
                        'desc': item.desc
                    })

                objCC = {
                    "category": category,
                    "items": list(arrProduct)
                }
                return response.ok(objCC, "Success")
            elif category == "PIC":
                loker = Loker.objects(Q(title__icontains=search) | Q(divisi__icontains=search) | Q(unit__icontains=search) | Q(sub_unit__icontains=search))
                objIdLoker = []
                for item in loker:
                    pic = Employe.objects(Q(name__icontains=search) | Q(loker=item.id))
                    if pic.count() > 0:
                        for emp in pic:
                            objIdLoker.append({
                                'nik' : emp.nik,
                                'name': emp.name,
                                'sub_unit': emp.loker.sub_unit,
                                'unit': emp.loker.unit,
                                'id_loker': str(emp.loker.id)
                            })

                objCC = {
                    "category": category,
                    "items": list(objIdLoker)
                }
                return response.ok(objCC, "Success")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def updateMapLog(id: str, request: Request) -> JSONResponse:
        try:
            body = await request.json()
            isPossible = body['possible']
            logs = Logs.objects(id=id).first()
            if logs is None:
                raise Exception('Logs tidak ditemukan!')

            logs.isMapDate = datetime.datetime.now()
            logs.isMapped = True
            logs.isPossibleMap = isPossible
            logs.save()

            return response.ok("Success", "Berhasil Update Logs apping")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def updateAliasPIC(request: Request) -> JSONResponse:
        try:
            body = await request.json()
            parameter = body['parameter']
            arr_loker = body['loker']

            for item in arr_loker:
                loker = Loker.objects(id=item['id_loker']).update_one(push__alias=parameter)

            return response.ok("Success", "Berhasil Update Logs apping")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def updateAliasProduct(request: Request) -> JSONResponse:
        try:
            body = await request.json()
            parameter = body['parameter']
            arr_product = body['product']

            for item in arr_product:
                product = Product.objects(id=item['id']).update_one(push__alias=parameter)

            return response.ok("Success", "Berhasil Update Logs apping")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def updateAliasCustomer(request: Request) -> JSONResponse:
        try:
            body = await request.json()
            parameter = body['parameter']
            arr_customer = body['customers']

            for item in arr_customer:
                cc = Cc.objects(id=item['id']).update_one(push__alias=parameter)

            return response.ok("Success", "Berhasil Update Logs apping")
        except Exception as e:
            return response.badRequest('', f'{e}')