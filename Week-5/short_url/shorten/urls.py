from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('url/<str:url_id>', views.redirect_to_original, name="url"),
]

