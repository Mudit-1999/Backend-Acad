from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import hashlib
from .models import Urls


# Create your views here.
def index(request):
    if request.method == 'POST':
        my_hash = hashlib.sha1(request.POST['original_url'].encode('utf-8')).hexdigest()
        Urls(url_id=my_hash[:10], original_url=request.POST['original_url']).save()
        messages.info(request, "Your short url is http://127.0.0.1:8000/url/" + my_hash[:10])
        return render(request, "index.html")
    else:
        return render(request, "index.html")


def redirect_to_original(request, url_id):
    try:
        url = Urls.objects.get(url_id=url_id)
        return redirect(url.original_url)
    except Urls.DoesNotExist:
        return HttpResponse("<h2>Unable to find url to redirect.\n Please check the url you have entered</h2>")

