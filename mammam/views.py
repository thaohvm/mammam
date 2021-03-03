from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.urls import reverse

# Create your views here.

def index(request):
    return render(request, "mammam/index.html")