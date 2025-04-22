from django.db import models

# Create your models here.
from django.db import models
from gadmin.models import Recycler

class RecyclerRequests(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("not_in_stock", "Not in Stock"),
    ]

    recycler = models.ForeignKey(Recycler, on_delete=models.CASCADE)
    garbage_details = models.JSONField()  # Store garbage type & weight as JSON
    pickup_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="pending")
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request {self.id} - {self.recycler.name} - {self.status}"
    


from django.db import models

class RecycledProducts(models.Model):
    recycler_id = models.PositiveIntegerField(default=1) # Ensure it's a number, not a string
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    supercoin_value = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='recycled_products/')
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

from django.db import models
class Complaint(models.Model):
    recycler_request = models.ForeignKey(RecyclerRequests, on_delete=models.CASCADE)
    complaint_text = models.TextField()
    is_solved = models.BooleanField(default=False)  # True for solved, False for pending/rejected
    filed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Solved" if self.is_solved else "Not Solved"
        return f"Complaint {self.id} - {self.recycler_request.recycler.name} ({status})"


