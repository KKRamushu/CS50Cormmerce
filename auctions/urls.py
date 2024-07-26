from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.addListing, name= "add"),
    path("listing/<str:item>", views.viewListing, name="listing"),
    path("closed/<str:item>", views.viewClosedListing, name="winner"),
    path("watchlist/<str:item>",views.addToWatchlist, name="watchlist"),
    path("viewWatchlist", views.viewWatchlist, name= "viewWatchlist"),
    path("removeWatchlist/<str:item>",views.removeFromWatchlist, name="removeWatchlist"),
    path("bid", views.placeBid, name="bid"),
    path("close", views.closeAuction, name="close"),
    path("viewClosed", views.closed, name="viewClosed"),
    path("comment", views.comment, name="comment")
]
