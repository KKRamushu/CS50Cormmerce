from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    def __str__(self):
        return f"{self.username}"



class Category(models.Model):
    category_name = models.CharField(max_length=30)
    def __str__(self):
        return f"{self.category_name}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    discription = models.CharField(max_length=600)
    imageUrl = models.CharField(max_length=1200)
    category =models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name="category")
    price = models.FloatField(max_length=8)
    seller= models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    active = models.BooleanField(default="True")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="cartlist")
    winner= models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="buyer")
    date = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return f"{self.title}"
    
class Comments(models.Model):
    comment = models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="customer")
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)
    date = models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return f"{self.id}"


class Bids(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="product")
    bid_price = models.FloatField(max_length=8)
    def __str__(self):
        return f"{self.bidder} : ${self.bid_price}"
