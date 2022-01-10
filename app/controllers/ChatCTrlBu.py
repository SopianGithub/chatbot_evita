from starlette.requests import Request
from starlette.responses import JSONResponse
from app import response
from mongoengine.queryset.visitor import Q

from app.models.cc import Cc, SegmenCC
from app.models.logs import Logs

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

def pagination(req):
    total = Cc.objects().count()
    action = req['queryResult']['action']
    page_start = 1
    page_size = 3
    # return {
    #     "fulfillmentText": "Mohon maaf Evita belum mengerti, Evita akan belajar lagi"
    # }
    contexts = [["pagination", 3, {"parameter": [page_start]}]]
    if action == "first_page":
        cc = Cc.objects().skip(page_start).limit(page_size)
        button = []
        for item in cc:
            button.append({
                "text": item.name,
                "postback": item.id_cc
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
                    "title": "Silahkan input nama cc atau nipnas",
                    "buttons": button
                },
                "platform": "TELEGRAM"
            }],
            "outputContexts": [
                {
                    "name": req['session']+"/contexts/pagination",
                    "lifespanCount": 5,
                    "parameters": {
                        "page-start": page_start
                    }
                }
            ]
        }
    elif action == "next" or action == "previous":
        output_context_list = req['queryResult']['outputContexts']
        for m in output_context_list:
            name = m["name"]
            w = "pagination"
            if name[-(len(w)):] == w:
                page_start = int(m['parameters']['page-start'])

        if action == "next":
            page_start += page_size
        elif action == "previous":
            page_start -= page_size

        cc = Cc.objects().skip(page_start).limit(page_size)

        button = []
        for item in cc:
            button.append({
                "text": item.name,
                "postback": item.id_cc
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
                    "title": "Silahkan input nama cc atau nipnas",
                    "buttons": button
                },
                "platform": "TELEGRAM"
            }],
            "outputContexts": [
                {
                    "name": req['session'] + "/contexts/pagination",
                    "lifespanCount": 5,
                    "parameters": {
                        "page-start": page_start
                    }
                }
            ]
        }
    else:
        return {
            "fulfillmentText": "Actiom Not Found"
        }

def processRequest(req):
    sessionID = req['session']
    result = req["queryResult"]
    intent = result["intent"]['displayName']
    # query_text = result["queryText"]
    # parameters = result["parameters"]
    # cust_name = parameters.get("cust_name")
    # cust_contact = parameters.get("cust_contact")
    # cust_email = parameters.get("cust_email")

    logs = Logs()
    logs.sessID = sessionID
    logs.parameter = req
    logs.intent = intent
    logs.save()

    if intent == 'customer':
        cc = listCC()
        return {
            "fulfillmentMessages": [
                {
                    "card": {
                        "title": "Silahkan input nama cc atau nipnas",
                        "buttons": cc['button_arr']
                    },
                    "platform": "TELEGRAM"
                }],
            "payload": {
                "paramscc" : {
                    "listcardcc" : cc['prmcc_arr']
                }
            }
        }
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