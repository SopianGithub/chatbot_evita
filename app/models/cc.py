from mongoengine import *

from app.models.am import Am

class SegmenCC(EmbeddedDocument):
    id_segmen = IntField(required=True)
    name = StringField(max_length=200, required=True)
    descr = StringField(max_length=500, required=True)

class Cc(Document):
    id_cc = IntField(primary_key=True, required=True)
    name = StringField(max_length=200, required=True)
    segmen = EmbeddedDocumentField(SegmenCC)
    alias = ListField(StringField(max_length=1000))
    mapping_am = ListField(ReferenceField(Am))