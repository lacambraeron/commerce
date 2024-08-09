from django.contrib import admin
from .models import Auction, Comment, WatchList, Bid

admin.site.register(Auction)
admin.site.register(Comment)
admin.site.register(WatchList)
admin.site.register(Bid)
# Register your models here.
