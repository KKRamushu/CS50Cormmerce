# Generated by Django 5.0.3 on 2024-04-25 19:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_remove_listing_bid_listing_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='bid',
        ),
        migrations.AddField(
            model_name='bids',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bidder', to='auctions.listing'),
        ),
    ]