from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import hashlib
from django.views.decorators.http import require_POST, require_GET
from .models import Urls
from django.views.decorators.csrf import csrf_exempt
from accounts.models import User
import json
import datetime


# Create your views here.
def validate_token(token=None):
    try:
        user = User.objects.get(token=token)
        return user
    except User.DoesNotExist:
        return None


def transform_data_into_json(urls):
    data = []
    for url in urls:
        data.append({
            'original_url': url.original_url,
            'mapped_url': 'http://127.0.0.1:8000/url/' + url.url_id
        })
    return json.dumps(data, indent=1)


@csrf_exempt
@require_POST
def delete_url(request):
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
        url_id = request.POST['short_url'].split("/")[-1]
        try:
            url = Urls.objects(url_id=url_id, token=token)
            url.delete()
            return HttpResponse("Url deleted")
        except Urls.DoesNotExist:
            return HttpResponse("No url found")
    else:
        return HttpResponse('Please sign in')


@csrf_exempt
@require_POST
def list_url(request):
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
        try:
            urls = Urls.objects(token=token)
            return HttpResponse(transform_data_into_json(urls))
        except Urls.DoesNotExist:
            return HttpResponse("No url found")
    else:
        return HttpResponse('Please sign in')


@csrf_exempt
@require_POST
def index(request):
    token = 'AU'
    if 'Authorization' in request.headers:
        token = request.headers['Authorization']
    original_url = request.POST['original_url']
    alias = request.POST['alias']
    token_required = True if (request.POST['token_required'] == 'True') else False

    print(token)

    if len(alias) == 0:
        alias = hashlib.sha1((original_url+token).encode('utf-8')).hexdigest()[:10]

    if Urls.objects(url_id=alias).limit(1).count():
        return HttpResponse("Alias already taken")

    user = validate_token(token=token)
    Urls(url_id=alias, original_url=original_url, token=token, token_required=token_required, user_id=user).save()
    return HttpResponse("Your short url is http://127.0.0.1:8000/url/" + alias)


def redirect_to_original(request, url_id):
    try:
        url = Urls.objects.get(url_id=url_id)
        token = 'AU'
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if url.token_required:
            if url.token != token and token != 'AU':
                return HttpResponse("Authorization token is wrong")
        Urls.objects.get(url_id=url_id).update(visit_counts=url.visit_counts+1, last_time_stamp=datetime.datetime.now)

        return HttpResponse(url.original_url)
    except Urls.DoesNotExist:
        return HttpResponse("<h2>Unable to find url to redirect.\n Please check the url you have entered</h2>")

