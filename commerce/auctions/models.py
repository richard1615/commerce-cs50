from turtle import ondrag
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = AbstractUser.username(maxlength = 10)
    password = AbstractUser.password(maxlength = 15)
    joined = AbstractUser.date_joined()


class Auc_listing(models.Model):
    name = models.CharField(max_length=20)
    starting_bid = models.IntegerField()
    img_url = models.URLField(max_length=200)
    category = models.CharField(max_length=20)
    desc = models.CharField(max_length=50)
    time = models.TimeField()
    date = models.DateField
    status = models.BooleanField()
    bids = models.ForeignKey(bids, on_delete = models.CASCADE)
    comments = models.ForeignKey(comments, on_delete = models.CASCADE)


class bids(models.Model):
    amount = models.IntegerField()
    time = models.Model()


class comments(models.Model):
    content = models.CharField(max_length=50)
    upvotes = models.IntegerField()