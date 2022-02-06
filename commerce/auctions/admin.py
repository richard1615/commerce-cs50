from django.contrib import admin

# Register your models here.
from .models import Auc_listing, bids, comments

admin.site.register(Auc_listing)
admin.site.register(bids)
admin.site.register(comments)