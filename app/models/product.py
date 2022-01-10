from mongoengine import *

class ProductFiles(EmbeddedDocument):
    type_file = StringField(max_length=500, required=True)
    url_file = ListField(URLField())

class Product(Document):
    name = StringField(max_length=100, required=True)
    desc = StringField(required=True)
    benefit = StringField(required=False)
    alias = ListField(StringField())
    productfile = ListField(EmbeddedDocumentField(ProductFiles));