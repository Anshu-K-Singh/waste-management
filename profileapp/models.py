from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

class Address(models.Model):
    HOME = 'Home'
    WORK = 'Work'
    OTHER = 'Other'
    
    ADDRESS_TYPES = [
        (HOME, 'Home'),
        (WORK, 'Work'),
        (OTHER, 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    address = models.CharField(max_length=255)
    address_type = models.CharField(
        max_length=10,
        choices=ADDRESS_TYPES,
        default=HOME
    )
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.address_type} - {self.address}, {self.city}, {self.state}"
    
    
    default = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if self.default:
            # Unset default for other addresses
            Address.objects.filter(user=self.user, default=True).update(default=False)
        super().save(*args, **kwargs)