from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import date, datetime
from django.db.models import Max

from .models import User, Auc_listing, comments, bids, Watchlist
from .forms import bid_form, listingForm, comment_form

def index(request):
    listings = Auc_listing.objects.filter(status = True)
    return render(request, "auctions/index.html", {
        'listings' : listings
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == 'POST':
            form = listingForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                starting_bid = form.cleaned_data['starting_bid']
                img_url = form.cleaned_data['img_url']
                category = form.cleaned_data['category']
                desc = form.cleaned_data['desc']
                time = datetime.now()
                date_today = date.today()
                user = request.user
                Auc_listing.objects.create(user = user, name = name, starting_bid = starting_bid, img_url = img_url, category = category, desc = desc, time = time)
                HttpResponseRedirect(reverse("index"))

    return render(request, 'auctions/create_listing.html', {
        'form': listingForm()
    })

def listing(request, lname):
    auction = Auc_listing.objects.filter(name = lname)[0]
    if request.method == 'POST':
        content = request.POST['content']
        user = request.user
        comments.objects.create(user = user, auction = auction, content = content)
    bids_form = bid_form()
    item = Auc_listing.objects.filter(name = lname)[0]
    comment = comment_form()
    comment_list = comments.objects.filter(auction = item)
    if request.user == item.user:
        if_current = 1
    else:
        if_current = 0
    count = bids.objects.filter(auction = auction).count()
    highest = bids.objects.filter(auction = auction).aggregate(Max('amount'))
    return render(request, 'auctions/listing.html', {
        'item' : item,
        'comment_form' : comment,
        'comment_list' : comment_list,
        'bid_form': bids_form,
        'if_current' : if_current,
        'user' : request.user,
        'count' : count,
        'highest' : highest
        })

def add_bid(request, lname):
    bid = request.POST['amount']
    user = request.user
    auction = Auc_listing.objects.filter(name = lname)[0]
    time = datetime.now()
    bids.objects.create(user = user, auction = auction, amount = bid, time = time)
    return HttpResponseRedirect(reverse("listing", args=[lname]))

def add_to_watchlist(request, lname):
    user = request.user
    auction = Auc_listing.objects.filter(name = lname)[0]
    Watchlist.objects.create(user = user, auction = auction)
    return HttpResponseRedirect(reverse("listing", args=[lname]))

def view_watchlist(request):
    items = Watchlist.objects.filter(user = request.user)
    return render(request, "auctions/watchlist.html", {
        'items' : items
    })

def close_auction(request, lname):
    auction = Auc_listing.objects.filter(name = lname)
    auction.update(status = False)
    return HttpResponseRedirect(reverse("index"))

def remove_from_watchlist(request, lname):
    auction = Auc_listing.objects.filter(name = lname)[0]
    Watchlist.objects.filter(auction = auction, user = request.user).delete()
    return HttpResponseRedirect(reverse("view_watchlist"))


