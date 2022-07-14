from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import hashlib
from .models import Urls


# Create your views here.
def index(request):
    if request.method == 'POST':
        original_url = request.POST['original_url']
        alias = request.POST['alias']
        print(len(alias))
        if len(alias) == 0:
            alias = hashlib.sha1((original_url+"").encode('utf-8')).hexdigest()[:10]

        if Urls.objects(url_id=alias).limit(1).count():
            messages.info(request, "Alias already taken")
            return redirect('/')
        Urls(url_id=alias, original_url=original_url).save()
        messages.info(request, "Your short url is http://127.0.0.1:8000/url/" + alias)
        return redirect('/')
    else:
        return render(request, "index.html")


def redirect_to_original(request, url_id):
    try:
        url = Urls.objects.get(url_id=url_id)
        return redirect(url.original_url)
    except Urls.DoesNotExist:
        return HttpResponse("<h2>Unable to find url to redirect.\n Please check the url you have entered</h2>")

