# Generated by Django 5.0.3 on 2024-05-30 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_alter_comments_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='date',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]