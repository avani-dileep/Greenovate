# In user/admin.py
from django.contrib import admin
from customer.models import UserProfile  # Import from the customer app

# Optionally, register the UserProfile model for admin
admin.site.register(UserProfile)
