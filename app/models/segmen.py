from mongoengine import *

class Segmen(Document):
    id_segmen = IntField(max_length=10, primary_key=True, required=True)
    name = StringField(max_length=200, required=True)
    descr = StringField(max_length=500, required=True)