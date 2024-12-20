"""
Users URLs
"""
from django.urls import path

from .views import send_message

urlpatterns = [
    path('send/', send_message),  # Define the 'send/' URL pattern for the send_message view
]
