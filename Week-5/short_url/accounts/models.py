from mongoengine import *
from mongoengine import signals
from rest_framework.authtoken.models import Token


# connect("my_db")
# Create your models here.
class User(Document):
    email = StringField(required=True)
    user_name = StringField(max_length=50, required=True)
    password = StringField(max_length=100, required=True)
    token = StringField(max_length=300)
