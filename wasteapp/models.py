from django.db import models
from django.contrib.auth.models import User
# Create your models here.

WASTE_TYPES = [
    ('Plastic', 'Plastic'),
    ('Organic', 'Organic'),
    ('Electronic', 'Electronic'),
    ('Metal', 'Metal'),
    ('Paper', 'Paper'),
]

class WasteRequest(models.Model):
    user = models.ForeignKey(User, related_name='waste_requests', on_delete=models.CASCADE)
    waste_type = models.CharField(max_length=50, choices=WASTE_TYPES)
    quantity = models.PositiveIntegerField(help_text="Enter quantity in kg")
    collection_time = models.DateTimeField()
    collection_location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default='Pending', choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.waste_type} - ({self.status})"