from dataclasses import field
import imp
from django.forms import ModelForm
from .models import Auc_listing, bids, comments


class listingForm(ModelForm):
    class Meta:
        model = Auc_listing
        fields = ['name', 'starting_bid', 'img_url', 'category', 'desc']

class comment_form(ModelForm):
    class Meta:
        model = comments
        fields = ['content']