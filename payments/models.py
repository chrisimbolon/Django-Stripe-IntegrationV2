from django.db import models
from django.shortcuts import render
from django.utils import timezone

class TherapySession(models.Model):
    """Available therapy session"""
    THERAPY_TYPES = [
        ('individual', 'individual_therapy'),
        ('couples','couples_therapy'),
        ('group','group_therapy'),
        ('family','family_therapy')
    ]
    
    title = models.CharField(max_length=200)
    therapy_type = models.CharField(max_length=50, choices=THERAPY_TYPES, default="individual")
    description = models.TextField
    duration = models.IntegerField(help_text="Duration in minutes")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in USD")
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['price']
    
    def __str__(self):
        return f"(self.title) - $(self.price)"
    
    def price_in_cent(self):
        """Stripe use cents"""
        return int(self.price * 100)

class Booking(models.Model):
    """User booking for therapy sessions"""
    STATUS_CHOICES =[
        ('pending','Pending Payment'),
        ('confirmed','Confirmed'),
        ('cancelled','Cancelled'),
        ('refunded','Refunded')
    ]

    session = models.ForeignKey(TherapySession, on_delete=models.CASCADE, related_name='bookings')
    user_name = models.CharField(max_length=200)
    user_email = models.EmailField()
    user_phone = models.CharField(max_length=20, blank=True)

    # Stripe Fields

    stripe_payment_intent_id = models.CharField(max_length=255, unique=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    booking_date = models.DateTimeField(default=timezone.now)
    confirmed_at = models.DateTimeField(null=True,blank=True)

    notes = models.TextField(blank=True,help_text="Additional notes from user")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user_name} - {self.session.title} {(self.status)}"
    
    def confirm_booking(self):
        """Confirm booking after successfull payment"""
        self.status = 'confirmed'
        self.confirmed_at = timezone.now()
        self.save()




class Payment(models.Model):
    """Track all payment transactions"""
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    stripe_payment_intent_id = models.CharField(max_length=255, unique=True)
    amount = models.IntegerField(help_text="Amount in cents") 
    currency = models.CharField(max_length=3, default="usd")
    status = models.CharField(max_length=50)

    stripe_charge_id = models.CharField(max_length=255, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.stripe_payment_intent_id} - {self.status}"