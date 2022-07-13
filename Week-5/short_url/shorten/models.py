from mongoengine import *


# Create your models here.



class URLS(Document):
    url_id = StringField(max_length=20, required=True)
    original_url = StringField(required=True)


