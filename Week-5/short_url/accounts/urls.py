from django.urls import path
from . import views

urlpatterns = [
    path("register", views.register, name="register"),
    path('login', views.signin, name="login"),
    path('delete_user', views.delete_user, name="delete_user"),
]