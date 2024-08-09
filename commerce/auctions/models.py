from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    pass


# class Auction Listings
class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    start_bid = models.DecimalField(max_digits=11, decimal_places=2) 
    current_bid = models.DecimalField(default=None, null=True, max_digits=11, decimal_places=2)
    closed_status = models.BooleanField(default=False)
    highest_bidder = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE, related_name="filter_highest_bidder")
    photo = models.URLField(null=True, default=None, max_length=500)
    category = models.TextField(max_length=50)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="filter_creator")
    winner = models.ForeignKey(User, null=True, blank=True, default=None, on_delete=models.CASCADE, related_name="filter_winning_user")
    created = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

# class Bids more like BidHistory for a listing
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="filter_user_bid")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="filter_bidon_auction")
    amount = models.DecimalField(max_digits=11, decimal_places=2)

    def __str__(self):
        return f"User: {self.user.username}, Amount: ${self.amount}"
    
# class comments
class Comment(models.Model):
    comment = models.TextField(max_length=1500)
    posted = models.DateField(auto_now=False, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="filter_comment_user")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="filter_comment_auction")

# class WatchList    
class WatchList(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="filter_watchlist_auction")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="filter_watchlist_user")