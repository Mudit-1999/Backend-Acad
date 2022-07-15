from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST, require_GET
from .models import User
from django.views.decorators.csrf import csrf_exempt
import hashlib
from django.http import HttpResponse


def generate_hash(key: str) -> str:
    return hashlib.sha256(key.encode('utf-8')).hexdigest()


def validate(username: str = None, password: str = None) -> User:
    try:
        user = User.objects.get(user_name=username)
        if user.password == password:
            return user
    except User.DoesNotExist:
        return None


def validate_new_user(user_name, email, password1, password2)-> str:
    if password1 != password2:
        return "Password doesn't match"
    if User.objects(user_name=user_name).limit(1).count():
        return "Username already taken"
    if User.objects(email=email):
        return "You are already registered. Please Sign In"
    return "Successful"


@csrf_exempt
@require_POST
def delete_user(request):
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
    else:
        return HttpResponse("Please sign in first or pass token")

    user = User.objects(token=token)
    user.delete()
    return HttpResponse("User Deleted\n Redirect to home page")


@csrf_exempt
@require_POST
def signin(request):
    user_name = request.POST['username']
    password = generate_hash(request.POST['password'])
    user = validate(user_name, password)
    if user is None:
        return HttpResponse("Invalid Credentials")
    return HttpResponse(user.token)



@csrf_exempt
@require_POST
def register(request):
    print("="*10, request)
    user_name = request.POST['username']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    email = request.POST['email']
    response = validate_new_user(user_name, email, password1, password2)
    if response != "Successful":
        messages.info(request, response)
        return HttpResponse(response)

    User(email=email, user_name=user_name, password=generate_hash(password1), token=generate_hash(user_name)).save()
    return HttpResponse('Please login')




