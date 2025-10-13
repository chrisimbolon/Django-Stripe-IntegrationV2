# payments/admin.py
from django.contrib import admin
from .models import TherapySession, Booking, Payment


@admin.register(TherapySession)
class TherapySessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'therapy_type', 'duration', 'price', 'available', 'created_at']
    list_filter = ['therapy_type', 'available']
    search_fields = ['title', 'description']
    list_editable = ['available']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'user_email', 'session', 'amount_paid', 'status', 'booking_date', 'created_at']
    list_filter = ['status', 'booking_date']
    search_fields = ['user_name', 'user_email', 'stripe_payment_intent_id']
    readonly_fields = ['stripe_payment_intent_id', 'confirmed_at', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user_name', 'user_email', 'user_phone', 'notes')
        }),
        ('Session Details', {
            'fields': ('session', 'booking_date')
        }),
        ('Payment Information', {
            'fields': ('stripe_payment_intent_id', 'amount_paid', 'status')
        }),
        ('Timestamps', {
            'fields': ('confirmed_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['stripe_payment_intent_id', 'booking', 'amount', 'currency', 'status', 'created_at']
    list_filter = ['status', 'currency']
    search_fields = ['stripe_payment_intent_id', 'stripe_charge_id']
    readonly_fields = ['created_at', 'updated_at']