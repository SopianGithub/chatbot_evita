from mongoengine import *

class Users(Document):
    nik = StringField(max_length=200, required=True, primary_key=True)
    name = StringField(max_length=200, required=True)
    password = StringField(max_length=200, required=True)