from django.db import models

# Create your models here.
from django.shortcuts import render

# Create your views here.
class Payment(models.Model):
    session_id = models.CharField(max_length=255, unique=True)
    customer_email = models.EmailField(null=True, blank=True)
    amount_total = models.IntegerField()  # amount in cents
    currency = models.CharField(max_length=10, default="usd")
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)