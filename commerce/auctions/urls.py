from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:auction_id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>/", views.category_listing, name='category_listing'),
    path("bids", views.bids, name="bids"),
    path("closed", views.closed, name="closed")

]