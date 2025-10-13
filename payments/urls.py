from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('session/<int:session_id>/', views.session_detail, name='session_detail'),
    # path('create-booking-intent/', views.create_booking_intent, name='create_booking_intent'),
    # path('booking/success/<int:booking_id>/', views.booking_success, name='booking_success'),
    # path('my-bookings/', views.my_bookings, name='my_bookings'),
    # path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
]