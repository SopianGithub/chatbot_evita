from mongoengine import *

class Am(Document):
    nik = StringField(max_length=10, primary_key=True, required=True)
    name = StringField(max_length=200, required=True)
    mobile = StringField(max_length=20, required=True)