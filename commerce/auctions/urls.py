from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.create_listing, name='createlisting'),
    path("listing/<str:lname>", views.listing, name="listing"),
    path("listing/<str:lname>/addbid", views.add_bid, name="add_bid"),
    path("watchlist", views.view_watchlist, name="view_watchlist"),
    path("add_to_watchlist/<str:lname>", views.add_to_watchlist, name='add_to_watchlist')
]

