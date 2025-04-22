from django.db import models
from customer.models import GarbagePickup  
from gadmin.models import Driver
class Complaint(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)  # Allow NULL values
    pickup = models.ForeignKey(GarbagePickup, on_delete=models.CASCADE, related_name='collector_complaints')
    complaint_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_solved = models.BooleanField(default=False) 

    def __str__(self):
        return f"Complaint against {self.driver.name if self.driver else 'Unknown'} - Pickup {self.pickup.id}"
