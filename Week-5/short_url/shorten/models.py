from mongoengine import *
from accounts.models import User
import datetime


class Urls(Document):
    url_id = StringField(max_length=20, required=True)
    original_url = StringField(required=True)
    token = StringField(max_length=300)
    token_required = BooleanField(default=False)
    user_id = ReferenceField(User, reverse_delete_rule=CASCADE)
    visit_counts = IntField(default=0)
    last_time_stamp = DateTimeField(default=datetime.datetime.now)