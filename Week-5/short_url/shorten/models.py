from mongoengine import *


class Urls(Document):
    url_id = StringField(max_length=20, required=True)
    original_url = StringField(required=True)


