import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import (
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Recipe


# Create your views here.


def index(request):
    return render(request, "mammam/index.html")


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "mammam/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "mammam/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "mammam/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "mammam/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "mammam/register.html")


@csrf_exempt
@login_required(login_url="/login")
def create(request):
    if request.method == "GET":
        return render(request, "mammam/create.html")
    elif request.method == "POST":
        data = json.loads(request.body)
        print('bbb')
        if request.FILES:
            print('aaa')

        ingredients = ', '.join(data['ingredients'])
        steps = ', '.join(data['steps'])

        recipe = Recipe(title=data['title'],
                        food_age=data['food-age'],
                        description='recipe-description',
                        user_id=request.user.id,
                        steps=steps,
                        ingredients=ingredients)
        recipe.save()

        return JsonResponse({"status": "OK"}, status=200)
