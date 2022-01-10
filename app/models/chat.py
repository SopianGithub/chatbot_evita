from mongoengine import *
from datetime import datetime

class Log(Document):
    sessionId = StringField(max_length=500, required=True)
    userIntent = StringField(max_length=200, required=True)
    userMessage = MultiLineStringField(required=True)
    botMessage = MultiLineStringField(required=True)
    potretDate = DateTimeField(default=datetime)

