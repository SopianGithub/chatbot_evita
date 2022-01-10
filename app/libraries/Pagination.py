from mongoengine.queryset.visitor import Q

from dialogflow_fulfillment import WebhookClient
from app.models.cc import Cc
from app.models.product import Product
from app.models.employe import Employe, Loker
from app.models.am import Am

class Pagination:
    total = 0
    page_start = 1
    page_size = 3
    titleMsg = ""
    data = []
    searchParams = ""
    buttonCard = []

    def __init__(self, agent: WebhookClient):
        action = agent.action
        self.data = []

        if action == "customer_page" or action == "product_page" or action == "pic_page" or action == "am_page" or agent.action == "next" or agent.action == "previous":
            if agent.action == "next" or agent.action == "previous":
                self.page_start = int(agent.context.get('pagination')['parameters']['page-start'])
                if agent.action == "next":
                    self.page_start += self.page_size - 1
                elif agent.action == "previous":
                    self.page_start -= self.page_size - 1

                contextact = agent.context.get('pagination')
                if 'params' in dict(contextact)['parameters']:
                    self.setParamsInput(dict(contextact)['parameters']['params'])

                self.pages(dict(contextact)['parameters']['category'], agent.action)

            else:
                self.pages(action)

        elif agent.intent == "Input":
            contextact = agent.context.get('pagination')
            self.setParamsInput(agent.parameters['params'])
            self.pages(dict(contextact)['parameters']['category'])

        else:
            self.titleMsg = 'Action Not Found'

    def setParamsInput(self, params):
        self.searchParams = params

    def pages(self, category, action = None):
        self.buttonCard = []
        if category == "customer_page":
            self.titleMsg = "Silahkan Pilih CC atau cari CC"
            if self.searchParams is None:
                self.total = Cc.objects().count()
                if action == "next" or action == "previous":
                    self.data = Cc.objects().skip(self.page_start).limit(self.page_size)
                else:
                    self.data = Cc.objects().skip(0).limit(self.page_size)
            else:
                self.total = Cc.objects(Q(alias__icontains=self.searchParams) | Q(
            name__icontains=self.searchParams)).count()
                if action == "next" or action == "previous":
                    self.data = Cc.objects(Q(alias__icontains=self.searchParams) | Q(
                        name__icontains=self.searchParams)).skip(self.page_start).limit(self.page_size)
                else:
                    self.data = Cc.objects(Q(alias__icontains=self.searchParams) | Q(
            name__icontains=self.searchParams)).skip(0).limit(self.page_size)
        elif category == "product_page":
            self.titleMsg = "Silahkan Pilih Product atau cari Product"
            if self.searchParams is None:
                self.total = Product.objects().count()
                if action == "next" or action == "previous":
                    self.data = Product.objects().skip(self.page_start).limit(self.page_size)
                else:
                    self.data = Product.objects().skip(0).limit(self.page_size)
            else:
                self.total = Product.objects(Q(alias__icontains=self.searchParams) | Q(
                name__icontains=self.searchParams)).count()
                if action == "next" or action == "previous":
                    self.data = Product.objects(Q(alias__icontains=self.searchParams) | Q(
                        name__icontains=self.searchParams)).skip(self.page_start).limit(self.page_size)
                else:
                    self.data = Product.objects(Q(alias__icontains=self.searchParams) | Q(
                name__icontains=self.searchParams)).skip(0).limit(self.page_size)
        elif category == "pic_page":
            self.titleMsg = "Silahkan Pilih PIC Job Desc atau cari PIC Job Desc"
            if self.searchParams is None:
                self.total = Employe.objects().count()
                if action == "next" or action == "previous":
                    self.data = Employe.objects().skip(self.page_start).limit(self.page_size)
                else:
                    self.data = Employe.objects().skip(0).limit(self.page_size)
            else:
                loker = Loker.objects(alias__icontains=self.searchParams)
                self.total = Employe.objects(Q(loker__in=loker) | Q(
                name__icontains=self.searchParams)).count()
                if action == "next" or action == "previous":
                    self.data = Employe.objects(Q(loker__in=loker) | Q(
                        name__icontains=self.searchParams)).skip(self.page_start).limit(self.page_size)
                else:
                    self.data = Employe.objects(Q(loker__in=loker) | Q(
                name__icontains=self.searchParams)).skip(0).limit(self.page_size)
        elif category == "am_page":
            self.titleMsg = "Silahkan Pilih Account Manager atau cari Account Manager"
            if self.searchParams is None:
                self.total = Am.objects().count()
                if action == "next" or action == "previous":
                    self.data = Am.objects().skip(self.page_start).limit(self.page_size)
                else:
                    self.data = Am.objects().skip(0).limit(self.page_size)
            else:
                self.total = Am.objects(Q(nik__icontains=self.searchParams) | Q(
                name__icontains=self.searchParams)).count()
                if action == "next" or action == "previous":
                    self.data = Am.objects(Q(nik__icontains=self.searchParams) | Q(
                        name__icontains=self.searchParams)).skip(self.page_start).limit(self.page_size)
                else:
                    self.data = Am.objects(Q(nik__icontains=self.searchParams) | Q(
                name__icontains=self.searchParams)).skip(0).limit(self.page_size)

        for item in self.data:
            keyItem = 0
            if category == "pic_page" or category == "am_page":
                keyItem = str(item.nik)
            elif category == "product_page":
                keyItem = str(item.id)
            elif category == "customer_page":
                keyItem = str(item.id_cc)

            self.buttonCard.append({
                "text": item.name+" \n",
                "postback": category+' ' + keyItem
            })

        if self.page_start + self.page_size >= self.total:
            self.buttonCard.append({
                "text": '<Previous',
                "postback": 'Previous'
            })
        elif self.page_start == 1:
            self.buttonCard.append({
                "text": 'Next>',
                "postback": 'Next'
            })
        else:
            self.buttonCard.append({
                "text": '<Previous',
                "postback": 'Previous'
            })
            self.buttonCard.append({
                "text": 'Next>',
                "postback": 'Next'})

