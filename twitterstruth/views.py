from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import HandleForm
from twython import Twython
import json

def index(request):
    if request.method == 'POST':
        form = HandleForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('success')
    else:
        form = HandleForm()

    return render(request, 'index.html', {'form': form})


def success(request):
    # Load credentials from json file
    with open("twitter_credentials.json", "r") as file:
        creds = json.load(file)

    # Instantiate an object
    python_tweets = Twython(creds['CONSUMER_KEY'], creds['ACCESS_TOKEN'])
    return HttpResponse("You entered a handle correctly")