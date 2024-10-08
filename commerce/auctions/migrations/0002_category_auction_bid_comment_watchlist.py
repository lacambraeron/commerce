# Generated by Django 5.0.2 on 2024-03-02 03:24

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=1000)),
                ('start_bid', models.DecimalField(decimal_places=2, max_digits=11)),
                ('current_bid', models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)),
                ('closed_status', models.BooleanField(default=False)),
                ('photo', models.TextField(default=None, max_length=500, null=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('auction_end', models.DateField(default=datetime.datetime(2024, 3, 9, 3, 24, 27, 962572, tzinfo=datetime.timezone.utc))),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filter_creator', to=settings.AUTH_USER_MODEL)),
                ('highest_bidder', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filter_highest_bidder', to=settings.AUTH_USER_MODEL)),
                ('winner', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filter_winning_user', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.category')),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=11)),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filter_bidon_auction', to='auctions.auction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filter_user_bid', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=1500)),
                ('posted', models.DateField(auto_now_add=True)),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filter_comment_auction', to='auctions.auction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filter_comment_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filter_watchlist_auction', to='auctions.auction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filter_watchlist_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
