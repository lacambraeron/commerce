# Generated by Django 5.0.2 on 2024-03-04 22:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_auction_auction_end_alter_auction_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='auction_end',
            field=models.DateField(default=datetime.datetime(2024, 3, 11, 22, 53, 20, 885928, tzinfo=datetime.timezone.utc)),
        ),
    ]
