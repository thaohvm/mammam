from django.contrib import admin

from .models import Image, Recipe, User

admin.site.register(Image)
admin.site.register(Recipe)
admin.site.register(User)
