from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User


def validate_user(user_name, email ,password1, password2)-> str:
    if password1 != password2:
        return "Password doesn't match"
    if User.objects(user_name=user_name).limit(1).count():
        return "Username already taken"
    if User.objects(email=email):
        return "You are already registered. Please Sign In"
    return "Successful"


# Create your views here.
def register(request):

    if request.method == 'POST':
        email = request.POST['email']
        user_name = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        response = validate_user(user_name, email, password1, password2)
        if response != "Successful":
            messages.info(request, response)
            return redirect('register')

        User(email=email, user_name=user_name, password=password1).save()
        return redirect('login')
    else:
        return render(request, "register.html")


def login(request):
    return render(request, "login.html")
