from starlette.requests import Request
from starlette.responses import JSONResponse
from mongoengine.queryset.visitor import Q

from app import response
from app.models.user import Users

class LoginController:
    @staticmethod
    async def login(request: Request) -> JSONResponse:
        try:
            body = await request.json()
            nik = body['nik']
            pwd = body['password']
            users = Users.objects(Q(nik=nik) & Q(password=pwd))
            messlogin = {
                "status": "Failed",
                "users": []
            }
            notif = "NIK atau Password kurang tepat"
            if users.count() > 0 :
                userlogin = {
                    "nik" : users[0]['nik'],
                    "name": users[0]['name']
                }
                notif = "Login Success"
                messlogin = {
                    "status": "Success",
                    "users": userlogin
                }

            return response.ok(messlogin, notif)
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def show(nik) -> JSONResponse:
        try:
            users = Users.objects(nik=nik)

            if users is None:
                raise Exception('Users tidak ditemukan!')

            return response.ok({
                "nik": users[0].nik,
                "name": users[0].name
            }, 'Success')
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def createUser(request: Request) -> JSONResponse:
        try:
            body = await request.json()
            nik = body['nik']
            pwd = body['password']
            name = body['name']

            user = Users()
            user.nik = nik
            user.name = name
            user.password = pwd
            user.save()

        except Exception as e:
            return response.badRequest('', f'{e}')