from mongoengine import *

class Usersbot(Document):
    id_telegram = IntField(primary_key=True, required=True)
    first_name = StringField(max_length=200, required=True)
    last_name = StringField(max_length=200, required=True)
    username = StringField(max_length=200, required=True)
    mobile = StringField(max_length=20)
    nik = StringField(max_length=20)
    isverify = BooleanField(default=False)