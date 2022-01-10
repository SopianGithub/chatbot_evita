from starlette.requests import Request
from starlette.responses import JSONResponse
from dialogflow_fulfillment import WebhookClient
from app.libraries.Pagination import Pagination
from app.libraries.DetailPage import DetailPage
from app.libraries.Login import Login
from app.models.logs import Logs
from app import response

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

def setLogging(agent: WebhookClient, isRespon = True):
    id_telegram = ""
    if 'data' in agent.original_request['payload']:
        if 'from' in agent.original_request['payload']['data']:
            id_telegram = agent.original_request['payload']['data']['from']['id']
        elif 'callback_query' in agent.original_request['payload']['data']:
            id_telegram = agent.original_request['payload']['data']['callback_query']['from']['id']

    logs = Logs()
    logs.sessID = agent.session
    logs.parameter = agent.parameters
    logs.intent = agent.intent

    contextact = {}
    if agent.context.get('pagination'):
        dcContAct = agent.context.get('pagination')['parameters']['category']
        contextact = dcContAct

    logs.context = str(contextact)
    logs.isResponse = isRespon
    logs.idTelegram = str(id_telegram)

    if id_telegram :
        logs.save()

def setOutputPage(agent: WebhookClient, cardTitle, cardList, page_num, action, params):
    fullfill = {}

    titleFin = cardTitle
    listCard = cardList
    if len(cardList) == 1 :
        titleFin = "Mohon maaf Evita belum mengerti, Evita akan belajar lagi."
        listCard = []

    if params != None:
        fullfill = {
            "fulfillmentMessages": [{
                "card": {
                    "title": titleFin,
                    "buttons": listCard
                },
                "platform": "TELEGRAM"
            }],
            "outputContexts": [
                {
                    "name": agent.session + "/contexts/pagination",
                    "lifespanCount": 50,
                    "parameters": {
                        "page-start": page_num,
                        "category": action,
                        "input": params
                    }
                }
            ]
        }
    else:
        fullfill = {
            "fulfillmentMessages": [{
                "card": {
                    "title": cardTitle,
                    "buttons": cardList
                },
                "platform": "TELEGRAM"
            }],
            "outputContexts": [
                {
                    "name": agent.session + "/contexts/pagination",
                    "lifespanCount": 50,
                    "parameters": {
                        "page-start": page_num,
                        "category": action
                    }
                }
            ]
        }

    return fullfill

def setOutputDetail(agent: WebhookClient, category):

    if category != 'product_page' :
        id = agent.parameters['id']
    else :
        id = agent.parameters['idprod']


    detailPage = DetailPage(category, id)

    return {
        "fulfillmentMessages": [
            {
                "card": {
                    "title": detailPage.webhookresponse,
                    "buttons": detailPage.cardResponse
                },
                "platform": "TELEGRAM"
            }
        ]
    }

def handler(agent: WebhookClient) -> None:
    page = Pagination(agent)

    if agent.intent == 'customer' or agent.intent == 'Product' or agent.intent == "AccountMgr" or agent.intent == "PICJobs":
        if agent.original_request['source'] == "telegram":
            isResponse = True
            if len(page.buttonCard) == 1:
                isResponse = False

            setLogging(agent, isResponse)

        return setOutputPage(agent, page.titleMsg, page.buttonCard, page.page_start, agent.action, None)

    elif agent.action == "next" or agent.action == "previous":
        if agent.original_request['source'] == "telegram":
            isResponse = True
            if len(page.buttonCard) == 1:
                isResponse = False

            setLogging(agent, isResponse)

        contextact = agent.context.get('pagination')
        if 'params' in dict(contextact)['parameters']:
            return setOutputPage(agent, page.titleMsg, page.buttonCard, page.page_start, agent.context.get('pagination')['parameters']['category'], dict(contextact)['parameters']['params'])
        else:
            return setOutputPage(agent, page.titleMsg, page.buttonCard, page.page_start, agent.context.get('pagination')['parameters']['category'], None)
    
    elif agent.intent == "Input":
        if agent.original_request['source'] == "telegram":
            isResponse = True
            if len(page.buttonCard) == 1:
                isResponse = False

            setLogging(agent, isResponse)

        # contextact = agent.context.get('pagination')
        return setOutputPage(agent, page.titleMsg, page.buttonCard, page.page_start, agent.context.get('pagination')['parameters']['category'], agent.parameters['params'])

    elif agent.intent == "Details":
        setLogging(agent, True)
        return setOutputDetail(agent, agent.parameters['paramspage'])

    elif agent.intent == "Main Menu":
        return mainMenu()

    else:
        setLogging(agent, False)
        return {
            "fulfillmentText": "Mohon maaf Evita belum mengerti, Evita akan belajar lagi "+agent.action
        }

class Conversation:

    @staticmethod
    async def index(request: Request) -> JSONResponse:
        req = await request.json()
        agent = WebhookClient(req)
        login = Login(agent)

        if login.verifiyAccess['status']:
            resfull = agent.handle_request(handler)
        else:
            resfull = login.prosesLoging(agent)

        return response.webhookres(resfull)
