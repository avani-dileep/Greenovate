from django.db import models
from django.conf import settings
  # or CustomUser if you're using a custom user model

class UserDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, default=None)  # Link to the User model
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
from recycler.models import RecycledProducts

from django.db import models
from django.conf import settings


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # Temporary fix
    product = models.ForeignKey(RecycledProducts, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def total_supercoins(self):
        return self.product.supercoin_value * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
  
from django.conf import settings

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('Online', 'Online Payment'),
        ('Supercoins', 'Supercoins Payment'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('complete', 'Complete'),
        ('reject', 'Rejected'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=15, choices=PAYMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - {self.payment_method}"
    
from django.db import models, transaction
from django.core.exceptions import ValidationError
  
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)  # ✅ Changed related_name
    product = models.ForeignKey(RecycledProducts, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Price in currency
    supercoin_value = models.PositiveIntegerField(default=0)  # Supercoins used

    def total_price(self):
        return self.price * self.quantity

    def total_supercoins(self):
        return self.supercoin_value * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"
    
   
    from django.db import models

    
from django.contrib.auth.models import User

class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username}"

