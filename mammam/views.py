import json
import re

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q
from django.http import (
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Image, Recipe, User


def index(request):
    query = request.GET.get("query", "")

    if query:
        # Preprocess query
        words = re.sub("[^A-Za-z0-9 ]+", "", query).lower().split()
        recipes = []
        for w in words:
            q = Q()
            q |= Q(title__contains=w)
            q |= Q(description__contains=w)
            q |= Q(description__contains=w)
            q |= Q(age__contains=w)
            q |= Q(ingredients__contains=w)
            q |= Q(steps__contains=w)
            recipes.extend(Recipe.objects.filter(q))
        recipes = recipes[:100]
    else:
        recipes = Recipe.objects.order_by("-created_at")[:10]

    return render(
        request,
        "index.html",
        {
            "action": "search" if query else "view",
            "query": query,
            "recipes": recipes,
        },
    )


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
                "login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "login.html")


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
                request, "register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


@csrf_exempt
def recipe(request, id):
    try:
        recipe = Recipe.objects.get(id=id)
    except Recipe.DoesNotExist:
        return HttpResponseNotFound("Recipe not found!")

    if request.method == "GET":
        ingredients = json.loads(recipe.ingredients)
        steps = json.loads(recipe.steps)

        return render(
            request,
            "view.html",
            {"recipe": recipe, "ingredients": ingredients, "steps": steps},
        )
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))
        if recipe.created_by != request.user:
            return JsonResponse(
                {
                    "status": "ERROR",
                    "message": "You're not the recipe's creator.",
                },
                status=403,
            )

        try:
            data = json.loads(request.POST.get("data"))
            files = request.FILES

            if "image" in files:
                # Need to delete the old image
                if recipe.image:
                    recipe.image.delete()
                # Then upload the new image
                image = Image(file=files["image"])
                image.save()

            recipe.title = data.get("title")
            if data.get("description", ""):
                recipe.description = data.get("description")
            if data.get("food-age", ""):
                recipe.age = data.get("food-age")
            recipe.ingredients = json.dumps(data.get("ingredients"))
            recipe.steps = json.dumps(data.get("steps"))
            recipe.image = image if "image" in files else recipe.image
            recipe.save()

            url = reverse("recipe", kwargs={"id": recipe.id})
            return JsonResponse(
                {"status": "OK", "url": url},
                status=200,
            )
        except Exception as e:
            return JsonResponse(
                {"status": "ERROR", "message": str(e)},
                status=500,
            )
    elif request.method == "DELETE":
        if not request.user.is_authenticated:
            return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))
        if recipe.created_by != request.user:
            return JsonResponse(
                {
                    "status": "ERROR",
                    "message": "You're not the recipe's creator.",
                },
                status=403,
            )
        if recipe.image:
            recipe.image.delete()
        recipe.delete()
        return JsonResponse({"status": "OK"}, status=200)
    else:
        return JsonResponse(
            {"status": "ERROR", "message": "Invalid method."},
            status=400,
        )


@csrf_exempt
@login_required(login_url="/login")
def create(request):
    if request.method == "GET":
        return render(request, "create.html")
    elif request.method == "POST":
        try:
            data = json.loads(request.POST.get("data"))
            files = request.FILES

            if "image" in files:
                image = Image(file=files["image"])
                image.save()

            recipe = Recipe(
                title=data.get("title"),
                description=data.get("description", ""),
                age=data.get("food-age", ""),
                ingredients=json.dumps(data.get("ingredients")),
                steps=json.dumps(data.get("steps")),
                image=image if "image" in files else None,
                created_by=request.user,
            )
            recipe.save()

            url = reverse("recipe", kwargs={"id": recipe.id})
            return JsonResponse(
                {"status": "OK", "url": url},
                status=200,
            )
        except Exception as e:
            return JsonResponse(
                {"status": "ERROR", "message": str(e)},
                status=500,
            )


@login_required(login_url="/login")
def update(request, id):
    try:
        recipe = Recipe.objects.get(id=id)
    except Recipe.DoesNotExist:
        return HttpResponseNotFound("Recipe not found!")

    if recipe.created_by != request.user:
        return HttpResponseForbidden()

    ingredients = json.loads(recipe.ingredients)
    steps = json.loads(recipe.steps)

    return render(
        request,
        "update.html",
        {"recipe": recipe, "ingredients": ingredients, "steps": steps},
    )
