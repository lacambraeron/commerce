from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django import forms

from .models import User, Auction, Comment, WatchList, Bid


#From Django forms (with help of CS50.ai)
class CreateListingForm(forms.Form):
    id = forms.HiddenInput()
    title = forms.CharField(label="Title")
    description = forms.CharField(widget=forms.Textarea, label="description")
    start_bid = forms.FloatField(label="Bid")
    start_bid.widget.attrs.update({'step': 'any'})
    category = forms.CharField(label="Categories")
    photo = forms.URLField(label="Image")

def index(request):
    #TODO DISPLAY LISTINGS
    active = Auction.objects.filter(closed_status=False)
    return render(request, "auctions/index.html", {
        "listings": active
    })

@login_required
def closed(request):
    closed = Auction.objects.filter(closed_status=True)
    return render(request, "auctions/closed.html", {
        "listings": closed
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
    
# create listing
@login_required
def create(request):
    if request.method == "POST":
        category = request.POST.get('category')
        new = Auction(title=request.POST['title'], 
                      description=request.POST['description'],
                      start_bid=float(request.POST['start_bid']),
                      current_bid = float(request.POST['start_bid']), 
                      creator = request.user, 
                      highest_bidder = None, 
                      winner = None, 
                      category = category, 
                      photo=request.POST['photo'], 
                      closed_status = False,
                      created = timezone.now())
        new.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        listing = CreateListingForm()
        return render(request,"auctions/create.html", {
            "form": listing
        })


# view a particular listing
@login_required
def listing(request, auction_id):
    message = None
    auction = get_object_or_404(Auction, pk=auction_id)
    comments = Comment.objects.filter(auction=auction)
    is_watching = WatchList.objects.filter(user=request.user, auction=auction).exists()
    is_creator = auction.creator == request.user
    is_winner = auction.winner
    bids = Bid.objects.filter(auction=auction)
    if auction.closed_status:
        #Cannot add to watch list
        #Cannot comment
        #Cannot bid
        #Can only remove from watch list
        if 'remove_watch_auction' in request.POST:
            # Remove auction from watchlist
            WatchList.objects.filter(user=request.user, auction=auction).delete()
            message = "Removed from watchlist."
            is_watching = False  # Update is_watching state
    # Render the listing page with a message indicating that the auction is closed
        return render(request, "auctions/listing.html", {
            "auction": auction,
            "comments": comments,
            "message": "This auction is closed.",
            "is_watching": is_watching,
            "is_creator": is_creator,
            "is_winner": is_winner,
            "bids": bids
        })
    if request.method == "POST":
        if 'bid_amount' in request.POST:
            bid_amount = request.POST.get("bid_amount")
            if bid_amount:
                if not auction.current_bid or float(bid_amount) > auction.current_bid:
                    auction.current_bid = float(bid_amount)
                    auction.highest_bidder = request.user
                    auction.save()
                    message = "Bid placed successfully."
                    # Create bid history
                    Bid.objects.create(user=request.user, auction=auction, amount=bid_amount)
                else:
                    message = "Bid amount must be higher than the current bid."
            else:
                message = "Please provide a valid bid amount."

        elif 'close_auction' in request.POST:
            # Close auction
            if not auction.closed_status:
                auction.closed_status = True
                auction.winner = auction.highest_bidder
                is_winner = auction.winner
                auction.save()
                message = "Auction closed successfully."

        elif 'remove_watch_auction' in request.POST:
            # Remove auction from watchlist
            WatchList.objects.filter(user=request.user, auction=auction).delete()
            message = "Removed from watchlist."
            is_watching = False  # Update is_watching state
        elif 'add_watch_auction' in request.POST:
            # Add auction to watchlist
            new_watch = WatchList.objects.create(user=request.user, auction=auction)
            new_watch.save()
            message = "Added to watchlist."
            is_watching = True  # Update is_watching state

        elif 'add_comment' in request.POST:
            comment_text = request.POST.get("add_comment")
            if comment_text:
                Comment.objects.create(user=request.user, auction=auction, comment=comment_text)
                messages.success(request, 'Comment added successfully.')
            else:
                messages.error(request, 'Please provide a valid comment.')
            return redirect('listing', auction_id=auction_id)

    # Check if the user is authenticated and watching the auction 
    return render(request, "auctions/listing.html", {
        "auction": auction,
        "comments": comments,
        "message": message,
        "is_watching": is_watching,
        "is_creator": is_creator,
        "is_winner": is_winner,
        "bids": bids
    })
# view list of auctions marked as watchlist
@login_required
def watchlist(request):
    # Retrieve the watchlist items for the current user
    watchlist_items = WatchList.objects.filter(user=request.user)
    
    # Extract the auctions from the watchlist items
    watchlist_auctions = [item.auction for item in watchlist_items]
    
    return render(request, "auctions/index.html", {
        "listings": watchlist_auctions
    })

# view a page of current categories
@login_required
def categories(request):
    # Retrieve unique categories from Auction model
    categories = Auction.objects.values_list('category', flat=True).distinct()
    return render(request, "auctions/categories.html", {
        "categories": categories
        })

@login_required
def category_listing(request, category):
    listings = Auction.objects.filter(category=category)
    return render(request, "auctions/category_listing.html", {
        'listings': listings,
        'category': category
        })

@login_required
def bids(request):
    # Get the listings bid history
    listings = Bid.objects.filter(user=request.user)
    return render(request, "auctions/bids.html", {"listings": listings})