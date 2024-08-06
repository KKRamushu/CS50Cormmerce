from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime

from .models import User, Category, Bids, Comments, Listing


def index(request):
    listings = Listing.objects.filter(active=True)
    activeListings = sorted(listings,key=lambda listings: listings.id, reverse=True)
    categories = Category.objects.all()
    if request.method == "POST":
        category = Category.objects.get(category_name=request.POST["category"])
        categoryListings = listings.filter(category=category)
        orderedListings = sorted(categoryListings,key=lambda categoryListings: categoryListings.id, reverse=True)
        return render(request, "auctions/index.html", {"activeListings": orderedListings, "categories": categories,
                                                       "activeCategory": category})
    else:
        return render(request, "auctions/index.html", {"activeListings": activeListings, "categories": categories,
                                                       "activeCategory": 'all'})

def closed(request):
    closedListings = Listing.objects.filter(active=False)
    return render(request, "auctions/closed.html",{"closedListings":closedListings})

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

def addListing(request):
        if request.method =="POST":
            inputTitle = request.POST["title"]
            inputDiscription = request.POST["discription"]
            inputImageUrl = request.POST["imageUrl"]
            inputPrice = request.POST["price"]
            inputCategory = None 
            if request.POST.get("category") and request.POST.get("category") != "Choose category":
                inputCategory = Category.objects.get(category_name=request.POST.get("category"))
               
            inputSeller = request.user
            now = datetime.now()
            date = now.strftime("%Y-%m-%d %H:%M")

            listing = Listing(
                title = inputTitle,
                discription = inputDiscription,
                category = inputCategory,
                imageUrl = inputImageUrl,
                price = float(inputPrice),
                seller = inputSeller,
                date = date

            )
            listing.save()

            return HttpResponseRedirect(reverse("index"))
        else:
            categories = Category.objects.all()
            return render(request, "auctions/add_listing.html", {"categories": categories})

def viewListing(request, item, massage = ""):
    userHighestBid = None
    listing = Listing.objects.get(title = item)
    inWatchList = request.user in listing.watchlist.all()
    bids = len(Bids.objects.filter(item = listing.id)) 
    seller = listing.seller
    if (request.user.is_authenticated) and (request.user != seller):
        listingBids = Bids.objects.filter(item = listing.id)
        userBids = listingBids.filter(bidder = request.user)
    
        if (userBids):
            userHighestBid = float( max(userBids.values_list("bid_price",flat=True)) )
        else:
            userHighestBid = 0

    comments = Comments.objects.filter(product = listing)
    commentsCount = len(comments)
    commentsList = sorted(comments,key=lambda comments: comments.id, reverse=True)
    return render(request, "auctions/listing.html", {"listing":listing, "inWatchList": inWatchList,
                                                      "bids":bids, "massage": massage, "comments": commentsList,
                                                      "noComments":commentsCount, "myBid": userHighestBid})
    pass

def viewClosedListing(request, item):
    listing = Listing.objects.get(title = item)
    return render(request, "auctions/closedListing.html", {"listing":listing})

def addToWatchlist(request, item):
    
    Listing.objects.get(title=item).watchlist.add(request.user)
    return viewListing(request,item)

def viewWatchlist(request):
    watchlistItems = Listing.objects.filter(watchlist = request.user)
    return render(request, "auctions/watchlist.html",{"watchlistItems": watchlistItems})

def removeFromWatchlist(request, item):
    
    Listing.objects.get(title=item).watchlist.remove(request.user)
    return viewListing(request,item)

def placeBid(request):
    if request.method == "POST":
        bidAmount = float(request.POST["bidAmount"])
        itemId = request.POST["item"]
        listing = Listing.objects.get(id=itemId)
        itemPrice = float(listing.price)
        bids = Bids.objects.filter(item = listing)
        if bids:
            maxBid = float( max(bids.values_list("bid_price",flat=True)) )
            if bidAmount > maxBid and bidAmount >= itemPrice:
                bid = Bids(bidder = request.user, item = listing, bid_price = bidAmount )
                bid.save()
                listing.price = bidAmount
                listing.save()
                listing.watchlist.add(request.user)
                massage = "success"
                return (viewListing(request,listing.title, massage))
            else:
                massage = "fail"
                return (viewListing(request,listing.title, massage))
        else:
            if bidAmount >= itemPrice:
                bid = Bids(bidder = request.user, item = listing, bid_price = bidAmount )
                newPrice = Listing(price = bidAmount)
                bid.save()
                listing.price = bidAmount
                listing.save()
                addToWatchlist(request, listing)
                massage = "Bid placed successfully"
                return (viewListing(request,listing.title, massage))
            else:
                massage = "Bid not placed, increase bid amount"
                return (viewListing(request,listing.title, massage))
            
def comment(request):
    if request.method == "POST":
        itemId = request.POST["item"]
        review = request.POST["comment"]
        listing = Listing.objects.get(id=itemId)
        user = request.user
        now = datetime.now()
        date = now.strftime("%Y-%m-%d %H:%M")
        comment = Comments(
            comment = review,
            user = user,
            product = listing,
            date = date
        )
        comment.save()
        return (viewListing(request,listing.title))

def closeAuction(request):
    if request.method == "POST":
        listing = Listing.objects.get(id=request.POST["listing"])
        bids = Bids.objects.filter(item = listing)
        maxBidPrice = float( max(bids.values_list("bid_price",flat=True)) )
        highestBid = bids.get(bid_price = maxBidPrice)
        listing.winner = highestBid.bidder
        listing.active = False
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    
