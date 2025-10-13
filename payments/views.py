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
