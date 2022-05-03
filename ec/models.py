from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Item(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    favorites = models.ManyToManyField(
        get_user_model(),
        through='Favorite'
    )


class Favorite(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)




