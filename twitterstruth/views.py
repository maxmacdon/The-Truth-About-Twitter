from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import HandleForm
import json


def index(request):
    username = ''
    if request.method == 'POST':
        form = HandleForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            with open("twitter_credentials.json", "r") as file:
                creds = json.load(file)
    else:
        form = HandleForm()

    return render(request, 'index.html', {'form': form, 'username': username})


