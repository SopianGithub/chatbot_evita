from dialogflow_fulfillment import WebhookClient
from mongoengine.queryset.visitor import Q
from app.models.usersbot import Usersbot
from app.models.employe import Employe
from app.models.am import Am

class Login:

    verifiyAccess = {
        "status": False
    }

    def __init__(self, agent: WebhookClient):

        if(self.checkingLogin(agent)):
            self.verifiyAccess = {
                "status": True
            }
        else:
            self.prosesLoging(agent)

    def checkingLogin(self, agent: WebhookClient):

        if agent.request_source == "telegram":
            if 'from' in agent.original_request['payload']['data']:
                id_telegram = agent.original_request['payload']['data']['from']
                self.verifiyAccess = self.CheckIsVerify(dict(id_telegram)['id'])
                return self.verifiyAccess['status']
            elif 'callback_query' in agent.original_request['payload']['data']:
                id_telegram = agent.original_request['payload']['data']['callback_query']['from']
                self.verifiyAccess = self.CheckIsVerify(dict(id_telegram)['id'])
                return self.verifiyAccess['status']
        elif (self.verifiyAccess['status']) or agent.request_source == "DIALOGFLOW_CONSOLE":
            return True
        else:
            return False

    def CheckIsVerify(self, id_telegram):
        userCheck = Usersbot.objects((Q(id_telegram=id_telegram) & Q(isverify=True))).count()
        if (userCheck > 0):
            return {
                "data": Usersbot.objects(id_telegram=id_telegram),
                "status": True
            }
        else:
            return {
                "status": False
            }

    def prosesLoging(self, agent: WebhookClient):
        if 'from' in agent.original_request['payload']['data']:
            origintTelegram = agent.original_request['payload']['data']['from']
            userBot = Usersbot()
            userBot.id_telegram = dict(origintTelegram)['id']
            userBot.username = dict(origintTelegram)['username']
            userBot.first_name  = dict(origintTelegram)['first_name']
            userBot.last_name   = dict(origintTelegram)['last_name']
            userBot.save()

        if agent.intent == "Login" or agent.intent == "Login_nik" or agent.intent == "Login_mobile":
            if agent.action == "input.login":
                return {
                    "fulfillmentText": "Silahkan Inputkan NIK kece kamu yang sudah terdaftar",
                    "outputContexts": [
                        {
                            "name": agent.session + "/contexts/Login",
                            "lifespanCount": 1,
                            "parameters": {
                                "nik": ""
                            }
                        }
                    ]
                }
            elif agent.action == "input.nik.login":
                return {
                    "fulfillmentText": "Silahkan Inputkan Nomor Ponsel Kamu, dengan kode area (+62)",
                    "outputContexts": [
                        {
                            "name": agent.session + "/contexts/Login",
                            "lifespanCount": 1,
                            "parameters": {
                                "nik": agent.parameters['niklogin']
                            }
                        }
                    ]
                }
            elif agent.action == "input.mobile.login":
                if 'from' in agent.original_request['payload']['data']:
                    id_telegram = agent.original_request['payload']['data']['from']
                elif 'callback_query' in agent.original_request['payload']['data']:
                    id_telegram = agent.original_request['payload']['data']['callback_query']['from']

                contextact = agent.context.get('login')
                if self.CheckProcessLogin(dict(contextact)['parameters']['niklogin.original'], agent.parameters['mobilelogin']):
                    userVer = Usersbot.objects(id_telegram=dict(id_telegram)['id']).first()
                    userVer.mobile = str(agent.parameters['mobilelogin'])
                    userVer.nik = dict(contextact)['parameters']['niklogin.original']
                    userVer.isverify = True
                    userVer.save()

                    return {
                        "fulfillmentText": "Selamat NIK Kamu Sudah Terverifikasi....",
                        "fulfillmentMessages": [{
                        "card": {
                            "title": "Selamat NIK Kamu Sudah Terverifikasi.... \nSilahkan Pilih Salah Satu Konteks Menu Chatbot Ini :",
                            "buttons": [
                                {
                                    "text": 'Corporate Customer',
                                    "postback": 'pagecc'
                                },
                                {
                                    "text": 'Account Manager',
                                    "postback": 'pageam'
                                },
                                {
                                    "text": 'PIC & Job Description',
                                    "postback": 'pagepic'
                                },
                                {
                                    "text": 'Product Solution',
                                    "postback": 'pageproduct'
                                }
                            ]
                        },
                        "platform": "TELEGRAM"
                    }],
                        "outputContexts": [
                            {
                                "name": agent.session + "/contexts/Login",
                                "lifespanCount": 1,
                                "parameters": {
                                    "nik": int(dict(contextact)['parameters']['nik']),
                                    "mobile": str(agent.parameters['mobilelogin'])
                                }
                            }
                        ]
                    }
                else:
                    return {
                        "fulfillmentText": "Nik dan No Handphone Tidak Terdaftar"+str(dict(contextact)['parameters']),
                        "outputContexts": [
                            {
                                "name": agent.session + "/contexts/Login",
                                "lifespanCount": 1,
                                "parameters": {
                                    "nik": dict(contextact)['parameters']['nik'],
                                    "mobile": str(agent.parameters['mobilelogin'])
                                }
                            }
                        ]
                    }
        else:
            return {
                "fulfillmentText": "Silahkan Inputkan NIK kece kamu yang sudah terdaftar",
                "outputContexts": [
                    {
                        "name": agent.session + "/contexts/Login",
                        "lifespanCount": 1,
                        "parameters": {
                            "nik": ""
                        }
                    }
                ]
            }

    def CheckProcessLogin(self, nik, mobile: str):
        employe = Employe.objects((Q(nik=int(nik)) and Q(mobile__icontains=str(mobile)))).count()
        if employe > 0:
            return True
        else:
            am = Am.objects((Q(nik=nik) and Q(mobile=mobile))).count()
            if am > 0:
                return True
            else:
                return False