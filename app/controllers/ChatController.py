from starlette.requests import Request
from starlette.responses import JSONResponse
from app import response
from mongoengine.queryset.visitor import Q

from app.models.cc import Cc, SegmenCC
from app.models.logs import Logs
from app.models.usersbot import Usersbot
from app.models.employe import Employe
from app.models.am import Am
from app.models.product import Product

def EntitySess(cat):
    entityarr = []
    if cat == "customer_page":
        data = Cc.objects()
        for valcc in data:
            tmp = {}
            tmp['value'] = valcc.name
            tmp['alias'] = valcc.alias
            entityarr.append(tmp)

    elif cat == "pic_page":
        data = Employe.objects()
        for valpic in data:
            tmp = {}
            tmp['value'] = valpic.name
            tmp['alias'] = valpic.loker.alias
            entityarr.append(tmp)

    elif cat == "product_page":
        data = Product.objects()
        for valprod in data:
            tmp = {}
            tmp['value'] = valprod.name
            tmp['alias'] = valprod.alias
            entityarr.append(tmp)

    return entityarr

def listCC():
    cc = Cc.objects().skip(0).limit(3)
    button = []
    prmcc = []
    for item in cc:
        button.append({
            "text": item.name,
            "postback": item.id_cc
        })

    button.append({
        "text": "More...",
        "postback": "Next+3"
    })
    prmcc.append({"Next": 3})

    return {
        "button_arr" : button,
        "prmcc_arr" : prmcc
    }

def customerMapping(queryResult):
    params = queryResult['parameters']
    nipnas = params['nipnasnum']
    alias = params['alias']
    # namacc = params['parametercc']
    loc_alias = params['loc_alias']

    webhookresponse = ""

    if(loc_alias != ''):
        query = Q(name__icontains=loc_alias[0]['business-name']) | Q(alias__icontains=loc_alias[0]['business-name'])
        cc = Cc.objects.filter(query)

    elif(alias != ''):
        cc = Cc.objects(alias__icontains = alias)

    elif(nipnas != ''):
        cc = Cc.objects(id_cc=nipnas)

    for item in cc:
        webhookresponse = "Nama Pelanggan : " + str(item.name) + \
                    "\n" + "Segmen : " + str(item.segmen.name)

    return webhookresponse

def mainMenu():
    return {
        "fulfillmentMessages": [{
            "card": {
                "title": "Silahkan Pilih Salah Satu Konteks Menu Chatbot Ini :",
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
        }]
    }

def pagination(req):
    total = 0
    action = req['queryResult']['action']
    page_start = 1
    page_size = 3
    if action == "customer_page" or action == "product_page" or action == "pic_page" or action == "am_page":
        button = []
        titleMsg = ""
        if action == "customer_page":
            total = Cc.objects().count()
            titleMsg = "Silahkan Pilih CC atau cari CC"
            cc = Cc.objects().skip(0).limit(page_size)
            for item in cc:
                button.append({
                    "text": item.name,
                    "postback": 'customer_page '+str(item.id_cc)
                })
        elif action == "product_page":
            total = Product.objects().count()
            titleMsg = "Silahkan Pilih Product atau cari Product"
            product = Product.objects().skip(0).limit(page_size)
            for item in product:
                button.append({
                    "text": item.name,
                    "postback": 'product_page '+str(item.id)
                })
        elif action == "pic_page":
            total = Employe.objects().count()
            titleMsg = "Silahkan Pilih PIC Job Desc atau cari PIC Job Desc"
            pic = Employe.objects().skip(0).limit(page_size)
            for item in pic:
                button.append({
                    "text": item.name,
                    "postback": 'pic_page '+str(item.nik)
                })
        elif action == "am_page":
            total = Am.objects().count()
            titleMsg = "Silahkan Pilih Account Manager atau cari Account Manager"
            ams = Am.objects().skip(0).limit(page_size)
            for item in ams:
                button.append({
                    "text": item.name,
                    "postback": 'am_page '+str(item.nik)
                })

        if total > page_start + page_size:
            button.append({
                "text": 'Next>',
                "postback": 'Next'
            })

        return {
            "fulfillmentMessages": [{
                "card": {
                    "title": titleMsg,
                    "buttons": button
                },
                "platform": "TELEGRAM"
            }],
            "outputContexts": [
                {
                    "name": req['session']+"/contexts/pagination",
                    "lifespanCount": 5,
                    "parameters": {
                        "page-start": page_start,
                        "category": action
                    }
                }
            ]
            # ,
            # "sessionEntityTypes": [
            #     {
            #         "name": req['session'] + "/entityTypes/" + action,
            #         "entities": EntitySess(action)
            #     }
            # ]
        }

    elif action == "next" or action == "previous":
        output_context_list = req['queryResult']['outputContexts']
        category = output_context_list[0]['parameters']['category']
        for m in output_context_list:
            name = m["name"]
            w = "pagination"
            if name[-(len(w)):] == w:
                page_start = int(m['parameters']['page-start'])

        if action == "next":
            page_start += page_size - 1
        elif action == "previous":
            page_start -= page_size - 1

        button = []
        titleMsg = ""
        if category == "customer_page":
            total = Cc.objects().count()
            titleMsg = "Silahkan Pilih CC atau cari CC"
            pageData = Cc.objects().skip(page_start).limit(page_size)
            for item in pageData:
                button.append({
                    "text": item.name,
                    "postback": 'customer_page '+str(item.id_cc)
                })
        elif category == "product_page":
            total = Product.objects().count()
            titleMsg = "Silahkan Pilih Product atau cari Product"
            pageData = Product.objects().skip(page_start).limit(page_size)
            for item in pageData:
                button.append({
                    "text": item.name,
                    "postback": 'product_page '+str(item.id)
                })
        elif action == "pic_page":
            total = Employe.objects().count()
            titleMsg = "Silahkan Pilih PIC Job Desc atau cari PIC Job Desc"
            pageData = Employe.objects().skip(page_start).limit(page_size)
            for item in pageData:
                button.append({
                    "text": item.name,
                    "postback": 'pic_page '+str(item.nik)
                })
        elif action == "am_page":
            total = Am.objects().count()
            titleMsg = "Silahkan Pilih Account Manager atau cari Account Manager"
            pageData = Am.objects().skip(page_start).limit(page_size)
            for item in pageData:
                button.append({
                    "text": item.name,
                    "postback": 'am_page '+str(item.nik)
                })

        if page_start + page_size >= total:
            button.append({
                "text": '<Previous',
                "postback": 'Previous'
            })
        elif page_start == 1:
            button.append({
                "text": 'Next>',
                "postback": 'Next'
            })
        else:
            button.append({
                "text": '<Previous',
                "postback": 'Previous'
            }, {"text": 'Next>',
                "postback": 'Next'})

        return {
            "fulfillmentMessages": [{
                "card": {
                    "title": titleMsg,
                    "buttons": button
                },
                "platform": "TELEGRAM"
            }],
            "outputContexts": [
                {
                    "name": req['session'] + "/contexts/pagination",
                    "lifespanCount": 5,
                    "parameters": {
                        "page-start": page_start,
                        "chcekCat" : category
                    }
                }
            ],
            "sessionEntityTypes": [
                {
                    "name": req['session'] + "/entityTypes/" + category,
                    "entities": EntitySess(category)
                }
            ]
        }
    else:
        return {
            "fulfillmentText": "Actiom Not Found"
        }

def detailCC(cc):
    for item in cc:
        webhookresponse = "Nama Pelanggan : " + str(item.name) + \
                          "\n" + "Segmen : " + str(item.segmen.name) + \
                          "\n \n Apakah Kamu Masih Membutuhkan Info Sesuatu?"

    return {
        "fulfillmentMessages": [
            {
                "card": {
                    "title": webhookresponse,
                    "buttons": [
                        {
                            "text": 'Ya',
                            "postback": 'Main Menu'
                        },
                        {
                            "text": 'Tidak',
                            "postback": 'close'
                        },
                    ]
                },
                "platform": "TELEGRAM"
            }
        ]
    }

def detailProduct(product):
    nameprod = ""
    desc = ""
    prodfile = []
    for item in product:
        nameprod = item.name
        desc = item.desc
        prodfile = item.productfile

    webhookresponse = "Product : " + str(nameprod) + \
                      "\nDescription : " + str(desc) + "\n"

    cardFile = []
    for filetipe in prodfile:
        for urlfile in filetipe.url_file:
            cardFile.append({
                "text": filetipe.type_file,
                "postback": urlfile
            })

    cardFile.append({
        "text": 'Menu Utama',
        "postback": 'Main Menu'
    })
    cardFile.append({
        "text": 'close Chat',
        "postback": 'close'
    })

    return {
        "fulfillmentMessages": [
            {
                "card": {
                    "title": webhookresponse,
                    "buttons": cardFile
                },
                "platform": "TELEGRAM"
            }
        ]
    }

def detailPic(pic):
    for item in pic:
        webhookresponse = "Nama PIC : " + str(item.name) + \
                          "\n" + "No.Kontak : " + str(item.mobile) + \
                          "\n \n"+ "Apakah Kamu Masih Membutuhkan Info Sesuatu?"

    return {
        "fulfillmentMessages": [
            {
                "card": {
                    "title": webhookresponse,
                    "buttons": [
                        {
                            "text": 'Ya',
                            "postback": 'Main Menu'
                        },
                        {
                            "text": 'Tidak',
                            "postback": 'close'
                        },
                    ]
                },
                "platform": "TELEGRAM"
            }
        ]
    }

def detailAm(am, id):
    for i in am:
        nama_am = i.name

    webhookresponse = "Nama AM : " + str(id) + \
                          "\n \n Apakah Kamu Masih Membutuhkan Info Sesuatu?"

    return {
        "fulfillmentMessages": [
            {
                "card": {
                    "title": webhookresponse,
                    "buttons": [
                        {
                            "text": 'Ya',
                            "postback": 'Main Menu'
                        },
                        {
                            "text": 'Tidak',
                            "postback": 'close'
                        },
                    ]
                },
                "platform": "TELEGRAM"
            }
        ]
    }

def detailPage(req):
    result = req["queryResult"]
    params = result['parameters']
    page_type = params['paramspage']
    id = params['id']
    idprod = params['idprod']
    if page_type == "customer_page":
        cc = Cc.objects(id_cc=id)
        return detailCC(cc)
    elif page_type == "product_page":
        product = Product.objects(id=idprod)
        return detailProduct(product)
    elif page_type == "pic_page":
        pic = Employe.objects(nik=id)
        return detailPic(pic)
    elif page_type == "am_page":
        am = Am.objects(nik=id)
        return detailAm(am, id)

def searchByInput(req):
    output_context_list = req['queryResult']['outputContexts']
    category = output_context_list[0]['parameters']['category']
    if category == "customer_page":
        msg = "Mohon maaf customer yang kamu cari tidak ketemu" + \
              "\n \n Apakah Kamu Masih Membutuhkan Info Sesuatu?"
        cc = Cc.objects(Q(alias__icontains=req['queryResult']['queryText']) | Q(
            name__icontains=req['queryResult']['queryText']))
        if cc is None:
            return {
                "fulfillmentMessages": [
                    {
                        "card": {
                            "title": msg,
                            "buttons": [
                                {
                                    "text": 'Ya',
                                    "postback": 'Main Menu'
                                },
                                {
                                    "text": 'Tidak',
                                    "postback": 'close'
                                },
                            ]
                        },
                        "platform": "TELEGRAM"
                    }
                ]
            }
        else:
            return detailCC(cc)
    elif category == "product_page":
        msg = "Mohon maaf product yang kamu cari tidak ketemu" + \
              "\n \n Apakah Kamu Masih Membutuhkan Info Sesuatu?"
        product = Product.objects(Q(alias__icontains=req['queryResult']['queryText']) | Q(
            name__icontains=req['queryResult']['queryText']))
        if product is None:
            return {
                "fulfillmentMessages": [
                    {
                        "card": {
                            "title": msg,
                            "buttons": [
                                {
                                    "text": 'Ya',
                                    "postback": 'Main Menu'
                                },
                                {
                                    "text": 'Tidak',
                                    "postback": 'close'
                                },
                            ]
                        },
                        "platform": "TELEGRAM"
                    }
                ]
            }
        else:
            return detailProduct(product)
    elif category == "pic_page":
        msg = "Mohon maaf PIC yang kamu cari tidak ketemu" + \
              "\n \n Apakah Kamu Masih Membutuhkan Info Sesuatu?"
        pic = Employe.objects(Q(alias__icontains=req['queryResult']['queryText']) | Q(
            name__icontains=req['queryResult']['queryText']))
        if pic is None:
            return {
                "fulfillmentMessages": [
                    {
                        "card": {
                            "title": msg,
                            "buttons": [
                                {
                                    "text": 'Ya',
                                    "postback": 'Main Menu'
                                },
                                {
                                    "text": 'Tidak',
                                    "postback": 'close'
                                },
                            ]
                        },
                        "platform": "TELEGRAM"
                    }
                ]
            }
        else:
            return detailPic(pic)

def CheckIsVerify(id_telegram):
    userCheck = Usersbot.objects( (Q(id_telegram=id_telegram) and Q(isverify=True)) ).count()
    if(userCheck > 0):
        return {
            "data" : Usersbot.objects(id_telegram=id_telegram),
            "status": True
        }
    else:
        return {
            "status": False
        }

def CheckLogin(nik, mobile):
    employe = Employe.objects( (Q(nik=nik) and Q(mobile=mobile)) ).count()
    if employe > 0 :
        return True
    else:
        am = Am.objects( (Q(nik=nik) and Q(mobile=mobile)) ).count()
        if am > 0 :
            return True
        else:
            return False

def processRequest(req):
    sessionID = req['session']
    result = req["queryResult"]
    intent = result["intent"]['displayName']

    if result['parameters'] != None:
        logs = Logs()
        logs.sessID = sessionID
        logs.parameter = result['parameters']
        logs.intent = intent
        logs.save()

    originInt = req['originalDetectIntentRequest']
    verifiyAccess = {
        "status": True
    }

    if req['originalDetectIntentRequest']['source'] == "telegram":
        if 'from' in req['originalDetectIntentRequest']['payload']['data']:
            id_telegram = req['originalDetectIntentRequest']['payload']['data']['from']
            verifiyAccess = CheckIsVerify(dict(id_telegram)['id'])
        elif 'callback_query' in req['originalDetectIntentRequest']['payload']['data']:
            id_telegram = req['originalDetectIntentRequest']['payload']['data']['callback_query']['from']
            verifiyAccess = CheckIsVerify(dict(id_telegram)['id'])

    if (verifiyAccess['status']) or req['originalDetectIntentRequest']['source'] == "DIALOGFLOW_CONSOLE":
        if intent == "Main Menu":
            return mainMenu()
        elif intent == 'customer' or intent == 'Product' or intent == "AccountMgr" or intent == "PICJobs":
            return pagination(req)
        elif intent == "Input":
            return searchByInput(req)
        elif intent == "Details":
            return detailPage(req)
        elif intent == "customer detail":
            return {
                "fulfillmentText": [customerMapping(result)]
            }
        elif intent == "First_Page" or intent == "Next" or intent == "Previous":
            return pagination(req)
        else:
            return {
                "fulfillmentText": "Mohon maaf Evita belum mengerti, Evita akan belajar lagi"
            }
    else:
        origintTelegram = originInt['payload']['data']['from']
        userBot = Usersbot()
        userBot.id_telegram = dict(origintTelegram)['id']
        userBot.username = dict(origintTelegram)['username']
        userBot.first_name = dict(origintTelegram)['first_name']
        userBot.last_name = dict(origintTelegram)['last_name']
        userBot.save()

        if intent == "Login" or intent == "Login_nik" or intent == "Login_mobile":
            action = req['queryResult']['action']
            if action == "input.login":
                return {
                    "fulfillmentText": "Silahkan Inputkan NIK kece kamu yang sudah terdaftar",
                    "outputContexts": [
                        {
                            "name": req['session'] + "/contexts/Login",
                            "lifespanCount": 1,
                            "parameters": {
                                "nik": ""
                            }
                        }
                    ]
                }
            elif action == "input.nik.login":
                return {
                    "fulfillmentText": "Silahkan Inputkan Nomor Ponsel Kamu...",
                    "outputContexts": [
                        {
                            "name": req['session'] + "/contexts/Login",
                            "lifespanCount": 1,
                            "parameters": {
                                "nik": req['queryResult']['parameters']['niklogin']
                            }
                        }
                    ]
                }
            elif action == "input.mobile.login":
                if CheckLogin(req['queryResult']['outputContexts'][0]['parameters']['nik'], req['queryResult']['parameters']['mobilelogin']):
                    userVer = Usersbot.objects(id_telegram=dict(id_telegram)['id']).first()
                    userVer.mobile = req['queryResult']['parameters']['mobilelogin']
                    # userVer.nik = req['queryResult']['outputContexts'][0]['parameters']['nik']
                    userVer.isverify = True
                    userVer.save()

                    return {
                        "fulfillmentText": "Selamat NIK Kamu Sudah Terverifikasi....",
                        "fulfillmentMessages": [
                            {
                                "card": {
                                    "title": "Silahkan Pilih Salah Satu Konteks Menu Chatbot Ini :",
                                    "buttons": [
                                        {
                                            "text": 'Corporate Customer',
                                            "postback": 'customer'
                                        },
                                        {
                                            "text": 'Account Manager',
                                            "postback": 'account'
                                        },
                                        {
                                            "text": 'PIC & Job Description',
                                            "postback": 'pic'
                                        },
                                        {
                                            "text": 'Product Solution',
                                            "postback": 'product'
                                        }
                                    ]
                                },
                                "platform": "TELEGRAM"
                        }],
                        "outputContexts": [
                            {
                                "name": req['session'] + "/contexts/Login",
                                "lifespanCount": 1,
                                "parameters": {
                                    "nik": req['queryResult']['outputContexts'][0]['parameters']['nik'],
                                    "mobile": req['queryResult']['parameters']['mobilelogin']
                                }
                            }
                        ]
                    }
                else :
                    return {
                        "fulfillmentText": "Nik dan No Handphone Tidak Terdaftar",
                        "outputContexts": [
                            {
                                "name": req['session'] + "/contexts/Login",
                                "lifespanCount": 1,
                                "parameters": {
                                    "nik": req['queryResult']['outputContexts'][0]['parameters']['nik'],
                                    "mobile": req['queryResult']['parameters']['mobilelogin']
                                }
                            }
                        ]
                    }
        else:
            return {
                "fulfillmentText": "Silahkan Inputkan NIK kece kamu yang sudah terdaftar",
                "outputContexts": [
                    {
                        "name": req['session'] + "/contexts/Login",
                        "lifespanCount": 1,
                        "parameters": {
                            "nik": ""
                        }
                    }
                ]
            }

class ChatController:

    @staticmethod
    async def webhook(request: Request) -> JSONResponse:
        try:
            req = await request.json()
            res = processRequest(req)
            return response.webhookres(res)
        except Exception as e:
            return response.badRequest('', f'{e}')


# def processRequest(req):
#
#     sessionID = req.get('responseId')
#     result = req.get("queryResult")
#     intent = result.get("intent").get('displayName')
#     query_text = result.get("queryText")
#     parameters = result.get("parameters")
#     cust_name = parameters.get("cust_name")
#     cust_contact = parameters.get("cust_contact")
#     cust_email = parameters.get("cust_email")
#
#     if intent == 'Main menu':
#         webhookresponse = ""
#
#
#     if intent == 'covid_searchcountry':
#         cust_country = parameters.get("geo-country")
#         if (cust_country == "United States"):
#             cust_country = "USA"
#
#         fulfillmentText, deaths_data, testsdone_data = makeAPIRequest(cust_country)
#         webhookresponse = "***Covid Report*** \n\n" + " New cases :" + str(fulfillmentText.get('new')) + \
#                           "\n" + " Active cases : " + str(
#             fulfillmentText.get('active')) + "\n" + " Critical cases : " + str(fulfillmentText.get('critical')) + \
#                           "\n" + " Recovered cases : " + str(
#             fulfillmentText.get('recovered')) + "\n" + " Total cases : " + str(fulfillmentText.get('total')) + \
#                           "\n" + " Total Deaths : " + str(deaths_data.get('total')) + "\n" + " New Deaths : " + str(
#             deaths_data.get('new')) + \
#                           "\n" + " Total Test Done : " + str(deaths_data.get('total')) + "\n\n*******END********* \n "
#         print(webhookresponse)
#         log.saveConversations(sessionID, cust_country, webhookresponse, intent, db)
#         log.saveCases("country", fulfillmentText, db)
#
#         return {
#
#             "fulfillmentMessages": [
#                 {
#                     "text": {
#                         "text": [
#                             webhookresponse
#                         ]
#
#                     }
#                 },
#                 {
#                     "text": {
#                         "text": [
#                             "Do you want me to send the detailed report to your e-mail address? Type.. \n 1. Sure \n 2. Not now "
#                             # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
#                         ]
#
#                     }
#                 }
#             ]
#         }
#     elif intent == "Welcome" or intent == "continue_conversation" or intent == "not_send_email" or intent == "endConversation" or intent == "Fallback" or intent == "covid_faq" or intent == "select_country_option":
#         fulfillmentText = result.get("fulfillmentText")
#         log.saveConversations(sessionID, query_text, fulfillmentText, intent, db)
#     elif intent == "send_report_to_email":
#         fulfillmentText = result.get("fulfillmentText")
#         log.saveConversations(sessionID, "Sure send email", fulfillmentText, intent, db)
#         val = log.getcasesForEmail("country", "", db)
#         print("===>", val)
#         prepareEmail([cust_name, cust_contact, cust_email, val])
#     elif intent == "totalnumber_cases":
#         fulfillmentText = makeAPIRequest("world")
#
#         webhookresponse = "***World wide Report*** \n\n" + " Confirmed cases :" + str(
#             fulfillmentText.get('confirmed')) + \
#                           "\n" + " Deaths cases : " + str(
#             fulfillmentText.get('deaths')) + "\n" + " Recovered cases : " + str(fulfillmentText.get('recovered')) + \
#                           "\n" + " Active cases : " + str(
#             fulfillmentText.get('active')) + "\n" + " Fatality Rate : " + str(
#             fulfillmentText.get('fatality_rate') * 100) + "%" + \
#                           "\n" + " Last updated : " + str(
#             fulfillmentText.get('last_update')) + "\n\n*******END********* \n "
#         print(webhookresponse)
#         log.saveConversations(sessionID, "Cases worldwide", webhookresponse, intent, db)
#         # log.saveCases("world", fulfillmentText, db)
#
#         return {
#
#             "fulfillmentMessages": [
#                 {
#                     "text": {
#                         "text": [
#                             webhookresponse
#                         ]
#
#                     }
#                 },
#                 {
#                     "text": {
#                         "text": [
#                             "Do you want me to send the detailed report to your e-mail address? Type.. \n 1. Sure \n 2. Not now "
#                             # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
#                         ]
#
#                     }
#                 }
#             ]
#         }
#
#     elif intent == "covid_searchstate":
#
#         fulfillmentText = makeAPIRequest("state")
#         print(len(fulfillmentText))
#
#         webhookresponse1 = ''
#         webhookresponse2 = ''
#         webhookresponse3 = ''
#         for i in range(0, 11):
#             webhookresponse = fulfillmentText[i]
#             # print(webhookresponse['state'])
#             # js = json.loads(webhookresponse.text)
#
#             # print(str(js.state))
#             webhookresponse1 += "*********\n" + " State :" + str(webhookresponse['state']) + \
#                                 "\n" + " Confirmed cases : " + str(
#                 webhookresponse['confirmed']) + "\n" + " Death cases : " + str(webhookresponse['deaths']) + \
#                                 "\n" + " Active cases : " + str(
#                 webhookresponse['active']) + "\n" + " Recovered cases : " + str(
#                 webhookresponse['recovered']) + "\n*********"
#         for i in range(11, 21):
#             webhookresponse = fulfillmentText[i]
#             # print(webhookresponse['state'])
#             # js = json.loads(webhookresponse.text)
#
#             # print(str(js.state))
#             webhookresponse2 += "*********\n" + " State :" + str(webhookresponse['state']) + \
#                                 "\n" + " Confirmed cases : " + str(
#                 webhookresponse['confirmed']) + "\n" + " Death cases : " + str(webhookresponse['deaths']) + \
#                                 "\n" + " Active cases : " + str(
#                 webhookresponse['active']) + "\n" + " Recovered cases : " + str(
#                 webhookresponse['recovered']) + "\n*********"
#         for i in range(21, 38):
#             webhookresponse = fulfillmentText[i]
#             # print(webhookresponse['state'])
#             # js = json.loads(webhookresponse.text)
#
#             # print(str(js.state))
#             webhookresponse3 += "*********\n" + " State :" + str(webhookresponse['state']) + \
#                                 "\n" + " Confirmed cases : " + str(
#                 webhookresponse['confirmed']) + "\n" + " Death cases : " + str(webhookresponse['deaths']) + \
#                                 "\n" + " Active cases : " + str(
#                 webhookresponse['active']) + "\n" + " Recovered cases : " + str(
#                 webhookresponse['recovered']) + "\n*********"
#         print("***World wide Report*** \n\n" + webhookresponse1 + "\n\n*******END********* \n")
#         print("***World wide Report*** \n\n" + webhookresponse2 + "\n\n*******END********* \n")
#         print("***World wide Report*** \n\n" + webhookresponse3 + "\n\n*******END********* \n")
#
#         log.saveConversations(sessionID, "Indian State Cases", webhookresponse1, intent, db)
#         return {
#
#             "fulfillmentMessages": [
#                 {
#                     "text": {
#                         "text": [
#                             webhookresponse1
#                         ]
#
#                     }
#                 },
#                 {
#                     "text": {
#                         "text": [
#                             webhookresponse2
#                         ]
#
#                     }
#                 },
#                 {
#                     "text": {
#                         "text": [
#                             webhookresponse3
#                         ]
#
#                     }
#                 },
#                 {
#                     "text": {
#                         "text": [
#                             "Do you want me to send the detailed report to your e-mail address? Type.. \n 1. Sure \n 2. Not now "
#                             # "We have sent the detailed report of {} Covid-19 to your given mail address.Do you have any other Query?".format(cust_country)
#                         ]
#
#                     }
#                 }
#             ]
#         }
#
#
#     else:
#         return {
#             "fulfillmentText": "something went wrong,Lets start from the begning, Say Hi",
#         }