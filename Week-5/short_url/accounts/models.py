from mongoengine import *


# Create your models here.
class User(Document):
    email = StringField(required=True)
    user_name = StringField(max_length=50)
    password = StringField(max_length=100)