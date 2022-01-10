from mongoengine import *

class Loker(Document):
    bp = StringField(max_length=10, required=True)
    title = StringField(max_length=500, required=True)
    divisi = StringField(max_length=500, required=True)
    unit = StringField(max_length=500, required=True)
    sub_unit = StringField(max_length=500, required=True)
    alias = ListField(StringField())

class Employe(Document):
    nik = IntField(primary_key=True, required=True)
    name = StringField(max_length=200, required=True)
    mobile = StringField(max_length=20, required=True)
    loker = ReferenceField(Loker)
