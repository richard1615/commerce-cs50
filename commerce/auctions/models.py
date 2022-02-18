from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Auc_listing(models.Model):
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    starting_bid = models.IntegerField()
    #highest_bid = models.IntegerField(default = 0)
    img_url = models.URLField(max_length=200)
    category = models.CharField(max_length=20)
    desc = models.CharField(max_length=50)
    time = models.TimeField()
    date = models.DateField
    status = models.BooleanField(default=True)

class bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auc_listing, on_delete=models.CASCADE)
    amount = models.IntegerField()
    time = models.TimeField()

class comments(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    auction = models.ForeignKey(Auc_listing, on_delete = models.CASCADE)
    content = models.CharField(max_length=50)
    upvotes = models.IntegerField(default=0)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    auction = models.ForeignKey(Auc_listing, on_delete = models.CASCADE)
    class Meta:
        unique_together = (('user', 'auction'),)
