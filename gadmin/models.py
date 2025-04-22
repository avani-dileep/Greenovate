from django.db import models

from django.db import models

class AdminUser(models.Model):
    email = models.EmailField(unique=True)
    
    password = models.CharField(max_length=255)  # Store as plain text

    def __str__(self):
        return self.email


class Driver(models.Model):
    driver_id = models.CharField(max_length=50, unique=True)  # Ensure it's unique
    name = models.CharField(max_length=100)
    aadhar_number = models.CharField(max_length=12, unique=True)
    address = models.TextField()
    driving_license_number = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=255)  # (Not recommended in production)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.driver_id} - {self.name}"

from django.db import models
class Recycler(models.Model):
    recycler_id = models.CharField(max_length=20, unique=True, primary_key=True)  # Set as primary key
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    company_name = models.CharField(max_length=100)
    address = models.TextField()
    password = models.CharField(max_length=128, blank=True, null=True)
 # Make sure password is included if needed



    def __str__(self):
        return f"{self.name} - {self.company_name}"
 
from django.db import models
from customer.models import GarbagePickup  # Importing from customer app
from gadmin.models import Driver

class DriverAssigned(models.Model):
    garbage_pickup = models.OneToOneField(GarbagePickup, on_delete=models.CASCADE)  # One pickup, one assignment
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    assigned_date = models.DateField(auto_now_add=True)

    def __str__(self):
        user = self.garbage_pickup.user
        driver_name = self.driver.name if self.driver else "No Driver Assigned"
        return f"{user.username} - Driver: {driver_name} - Status: {self.get_status_display()}"
