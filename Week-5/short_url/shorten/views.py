from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import messages
import hashlib
from django.views.decorators.http import require_POST, require_GET
from .models import Urls
from django.views.decorators.csrf import csrf_exempt
from accounts.models import User
import json
import datetime
from typing import Any


# Create your views here.
def generate_hash(key: str) -> str:
    return hashlib.sha256(key.encode('utf-8')).hexdigest()


def get_new_alias(original_url: str, token: str, alias: str) ->str:
    if len(alias) == 0:
        return hashlib.sha1((original_url+token).encode('utf-8')).hexdigest()[:10]
    return alias


def validate_token(token: str = None) -> Any:
    try:
        user = User.objects.get(token=token)
        return user
    except User.DoesNotExist:
        return None


def transform_data_into_json(urls: Urls) -> json:
    data = []
    for url in urls:
        data.append({
            'original_url': url.original_url,
            'mapped_url': 'http://127.0.0.1:8000/url/' + url.url_id
        })
    return json.dumps(data, indent=1)


def handle_delete_url(token: str, url_id: str) -> HttpResponse:
    try:
        url = Urls.objects(url_id=url_id, token=token)
        url.delete()
        return HttpResponse("Url deleted")
    except Urls.DoesNotExist:
        return HttpResponseBadRequest


def handle_list_url(token: str) -> HttpResponse:
    try:
        urls = Urls.objects(token=token)
        return HttpResponse(transform_data_into_json(urls))
    except Urls.DoesNotExist:
        return HttpResponseBadRequest


def handle_shortening(original_url: str, alias: str, token: str, token_required: bool):

    alias = get_new_alias(original_url=original_url, alias=alias, token=token)
    if Urls.objects(url_id=alias).limit(1).count():
        return HttpResponse("Alias already taken")
    user = validate_token(token=token)
    Urls(url_id=alias, original_url=original_url, token=token, token_required=token_required, user_id=user).save()
    return HttpResponse("Your short url is http://127.0.0.1:8000/url/" + alias)


def check_authorization(request, url: User) -> HttpResponse:
    if 'Authorization' not in request.headers:
        return HttpResponse("Please provide authorization token")
    if url.token != generate_hash(request.headers['Authorization']):
        return HttpResponse("Authorization token is wrong")
    return update_fields_and_send_response(url)


def update_fields_and_send_response(url: User) -> HttpResponse:
    Urls.objects.get(url_id=url.url_id).update(visit_counts=url.visit_counts + 1, last_time_stamp=datetime.datetime.now)
    return redirect(url.original_url)


@csrf_exempt
def redirect_to_original(request, url_id: str) -> HttpResponse:
    try:
        url = Urls.objects.get(url_id=url_id)
        if url.token_required:
            return check_authorization(request=request, url=url)
        return update_fields_and_send_response(url)
    except Urls.DoesNotExist:
        raise Http404


@csrf_exempt
@require_POST
def shorten_url(request):
    token = 'AU'
    if 'Authorization' in request.headers:
        token = generate_hash(request.headers['Authorization'])
    original_url = request.POST['original_url']
    alias = request.POST['alias']
    token_required = True if (request.POST['token_required'] == 'True' and token != 'AU') else False

    return handle_shortening(original_url=original_url, alias=alias, token=token, token_required=token_required)


@csrf_exempt
@require_POST
def delete_url(request):
    if 'Authorization' in request.headers:
        token = generate_hash(request.headers['Authorization'])
        url_id = request.POST['short_url'].split("/")[-1]
        return handle_delete_url(token=token, url_id=url_id)
    else:
        return HttpResponse('Please sign in')


@csrf_exempt
@require_POST
def list_url(request):
    if 'Authorization' in request.headers:
        token = generate_hash(request.headers['Authorization'])
        return handle_list_url(token=token)
    else:
        return HttpResponse('Please sign in')


