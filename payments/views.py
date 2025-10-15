from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils import timezone
from .models import TherapySession
import stripe
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    """Homepage - List of available sessions"""
    sessions = TherapySession.objects.filter(available = True)
    context = {
        'sessions' : sessions,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'sessions_list.html', context)

def session_detail(request, session_id):
    """Detail page for a specific therapy session"""
    session = get_object_or_404(TherapySession, id=session_id, available=True)
    context = {
        'session': session,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'session_detail.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def create_booking_intent(request):
    """
    Create a Payment Intent and Booking record
    This is called when user clicks "Book & Pay"
    """
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        user_name = data.get('name')
        user_email = data.get('email')
        user_phone = data.get('phone', '')
        notes = data.get('notes', '')
        
        # Get the therapy session
        session = TherapySession.objects.get(id=session_id, available=True)
        
        # Create Stripe Payment Intent
        intent = stripe.PaymentIntent.create(
            amount=session.price_in_cents(),
            currency='usd',
            metadata={
                'session_id': session.id,
                'session_title': session.title,
                'user_name': user_name,
                'user_email': user_email,
            }
        )
        
        # Create Booking record (pending)
        booking = Booking.objects.create(
            session=session,
            user_name=user_name,
            user_email=user_email,
            user_phone=user_phone,
            notes=notes,
            stripe_payment_intent_id=intent.id,
            amount_paid=session.price,
            status='pending'
        )
        
        # Create Payment record
        Payment.objects.create(
            booking=booking,
            stripe_payment_intent_id=intent.id,
            amount=session.price_in_cents(),
            currency='usd',
            status='pending'
        )
        
        return JsonResponse({
            'clientSecret': intent.client_secret,
            'booking_id': booking.id
        })
        
    except TherapySession.DoesNotExist:
        return JsonResponse({'error': 'Session not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def booking_success(request, booking_id):
    """Success page after payment"""
    booking = get_object_or_404(Booking, id=booking_id)
    context = {
        'booking': booking
    }
    return render(request, 'booking_success.html', context)


def my_bookings(request):
    """View user's bookings (simple version - by email query param)"""
    email = request.GET.get('email', '')
    bookings = []
    
    if email:
        bookings = Booking.objects.filter(user_email=email).select_related('session')
    
    context = {
        'bookings': bookings,
        'email': email
    }
    return render(request, 'my_bookings.html', context)


@csrf_exempt
def stripe_webhook(request):
    """
    Handle Stripe webhooks
    This is where we confirm bookings after successful payment
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        
        print("🎸 PAYMENT SUCCEEDED!")
        print(f"   Payment Intent ID: {payment_intent['id']}")
        print(f"   Amount: ${payment_intent['amount']/100}")
        
        try:
            # Find the booking
            booking = Booking.objects.get(
                stripe_payment_intent_id=payment_intent['id']
            )
            
            # Confirm the booking
            booking.confirm_booking()
            
            # Update payment record
            payment = Payment.objects.get(
                stripe_payment_intent_id=payment_intent['id']
            )
            payment.status = 'succeeded'
            payment.stripe_charge_id = payment_intent.get('latest_charge', '')
            payment.save()
            
            print(f"   ✅ Booking #{booking.id} confirmed for {booking.user_name}")
            
            # Here you would send confirmation email
            # send_booking_confirmation_email(booking)
            
        except Booking.DoesNotExist:
            print(f"   ⚠️  Booking not found for payment intent: {payment_intent['id']}")
        
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        print(f"💥 Payment failed: {payment_intent['id']}")
        
        try:
            payment = Payment.objects.get(
                stripe_payment_intent_id=payment_intent['id']
            )
            payment.status = 'failed'
            payment.save()
        except Payment.DoesNotExist:
            pass
    
    return HttpResponse(status=200)