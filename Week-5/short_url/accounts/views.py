# from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from .models import User
from django.views.decorators.csrf import csrf_exempt
import hashlib
from django.http import HttpResponse, HttpResponseBadRequest


fixed_string = "MUDIT"


def generate_hash(key: str) -> str:
    return hashlib.sha256(key.encode('utf-8')).hexdigest()


def validate(username: str = None, password: str = None) -> HttpResponse:
    try:
        user = User.objects.get(user_name=username)
        if user.password == password:
            return HttpResponse(generate_hash(username + fixed_string + password))
        return HttpResponseBadRequest
    except User.DoesNotExist:
        return HttpResponseBadRequest


def validate_new_user(user_name: str, email: str)-> str:
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
    password = generate_hash(request.POST['password'] + fixed_string)
    return validate(user_name, password)



@csrf_exempt
@require_POST
def register(request):
    print("="*10, request)
    user_name = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    response = validate_new_user(user_name, email)
    if response != "Successful":
        return HttpResponse(response)
    User(
        email=email,
        user_name=user_name,
        password=generate_hash(password + fixed_string),
        token=generate_hash(generate_hash(user_name + fixed_string + password))
    ).save()

    return HttpResponse('Please login')




