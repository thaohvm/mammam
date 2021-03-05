from django.contrib.auth.models import AbstractUser
from django.db import models
from star_ratings.models import Rating

class User(AbstractUser):
    pass


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=1000, blank=True)
    ingredient = models.TextField(max_length=500, blank=True)
    step = models.TextField(max_length=4000, blank=True)
    image = models.ImageField(upload_to="uploads/images",blank=True)
    
