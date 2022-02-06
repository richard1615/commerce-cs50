from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Auc_listing(models.Model):
    user = models.ManyToManyField(User, blank=True, related_name="auctions")
    name = models.CharField(max_length=20)
    starting_bid = models.IntegerField()
    img_url = models.URLField(max_length=200)
    category = models.CharField(max_length=20)
    desc = models.CharField(max_length=50)
    time = models.TimeField()
    date = models.DateField
    status = models.BooleanField()

class bids(models.Model):
    user = models.ManyToManyField(User, blank=True, related_name="bids")
    auction = models.ManyToManyField(Auc_listing, blank=True, related_name="bids")
    amount = models.IntegerField()
    time = models.TimeField()

class comments(models.Model):
    user = models.ManyToManyField(User, blank=True, related_name="comments")
    auction = models.ManyToManyField(Auc_listing, blank=True, related_name="comments")
    content = models.CharField(max_length=50)
    upvotes = models.IntegerField()