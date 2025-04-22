from django.conf import settings
from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser
from dateutil.relativedelta import relativedelta

# Custom User Model
class CustomUser(AbstractUser):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, default=None)
    phone = models.CharField(max_length=15, blank=False)
    email = models.EmailField(unique=True)
    building = models.CharField(max_length=100)
    flat_number = models.CharField(max_length=10)
    profile_picture = models.ImageField(
        upload_to='customer/',
        blank=True,
        null=True,
        default='customer/defaultavatar.jpg'
    )
    pass

    def __str__(self):
        return self.username
    
# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    supercoins = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username

    @property
    def name(self):
        return self.user.username or 'No Name Provided'

    @property
    def flat_number(self):
        return self.user.flat_number or 'Not Provided'

from django.utils import timezone

class GarbagePickup(models.Model):
    PICKUP_FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('special', 'Special Event'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
    ]
    PAYMENT_STATUS_CHOICES = [
        (0, 'Not Paid'),
        (1, 'Paid'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pickup_date = models.DateField(null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True)
    frequency = models.CharField(max_length=10, choices=PICKUP_FREQUENCY_CHOICES)
    remarks = models.TextField(blank=True, null=True)
    total_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subscription_start_date = models.DateTimeField(default=timezone.now)   # Automatically set to creation date
    subscription_end_date = models.DateField(null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)
    points = models.PositiveIntegerField(default=0)  # Store points
    supercoins = models.PositiveIntegerField(default=0)  # Store supercoins
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    payment_status = models.IntegerField(choices=PAYMENT_STATUS_CHOICES, default=0)  # Payment status field

    def calculate_payment(self):
        base_payment = 0
        additional_charge = 0

        # Base payment calculation based on frequency
        if self.frequency == 'daily':
            base_payment = 30 * 30 * self.duration
        elif self.frequency == 'weekly':
            base_payment = 100 * 4 * self.duration
        elif self.frequency == 'monthly':
            base_payment = 300 * self.duration
        elif self.frequency == 'special':
            base_payment = 50

        # Additional charge based on weight
        if self.weight is not None:
            additional_charge = max(0, self.weight) * 10  # Display rate is based on weight * 10
        
        # Calculate total payment (for storage purposes)
        total_payment = base_payment + additional_charge
        self.total_payment = total_payment

        # Subscription end date calculation
        if self.frequency != 'special' and self.pickup_date:
            end_date = self.pickup_date + relativedelta(months=self.duration)
            self.subscription_end_date = end_date
        else:
            self.subscription_end_date = None  # Special events do not have subscription end date

    def update_user_points_and_supercoins(self):
        """Update the user's total points and supercoins."""
        user_profile = self.user.userprofile
        user_profile.points += self.points
        user_profile.supercoins += self.supercoins
        user_profile.save()

# models.py

from django.db import models
from django.conf import settings

class Complaint(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link the complaint to a user
    pickup_schedule = models.ForeignKey('GarbagePickup', on_delete=models.CASCADE)  # Link to a specific pickup schedule
    complaint_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_solved = models.BooleanField(default=False)  # Added status field to track if the complaint is solved

    def __str__(self):
        return f"Complaint by {self.user.username} on {self.created_at}"

