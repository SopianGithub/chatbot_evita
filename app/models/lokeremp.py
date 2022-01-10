from mongoengine import *

class Lokeremp(Document):
    divisi = StringField(max_length=500, required=True)
    level = DictField()