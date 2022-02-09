from tracemalloc import start
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .models import User, Auc_listing, comments
from .forms import listingForm, comment_form

def index(request):
    listings = Auc_listing.objects.all()
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
                user = request.user
                Auc_listing.objects.create(user = user, name = name, starting_bid = starting_bid, img_url = img_url, category = category, desc = desc)
                HttpResponseRedirect(reverse("index"))

    return render(request, 'auctions/create_listing.html', {
        'form': listingForm()
    })

def listing(request, lname):
    if request.method == 'POST':
        content = request.POST['content']
        user = request.user
        auction = item = Auc_listing.objects.filter(name = lname)[0]
        comments.objects.create(user = user, auction = auction, content = content)
    item = Auc_listing.objects.filter(name = lname)[0]
    comment = comment_form()
    comment_list = comments.objects.filter(auction = item)
    return render(request, 'auctions/listing.html', {
        'item' : item,
        'comment_form' : comment,
        'comment_list' : comment_list
    })