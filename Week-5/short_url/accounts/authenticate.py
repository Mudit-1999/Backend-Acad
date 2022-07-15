from django.contrib.auth.backends import BaseBackend
from .models import User


class MyBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        user = User.objects.get(user_name=username)
        if user.password == password:
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(username=user_id)
        except User.DoesNotExist:
            return None
