import datetime
from mongoengine import *

class Logs(Document):
    potretdate = DateTimeField(default=datetime.datetime.now)
    intent = StringField()
    parameter = DictField()
    sessID = StringField()
    context = StringField()
    isResponse = BooleanField()
    idTelegram = StringField()
    isMapped = BooleanField()
    isPossibleMap = BooleanField()
    isMapDate = DateTimeField()