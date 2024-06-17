from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('maker', 'Maker'),
        ('checker', 'Checker'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    # otp=models.CharField(max_length=6)
    selected_checker = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='makers_as_checker')
    
    def __str__(self):
        return self.username
    
class Customer(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    photo = models.ImageField(upload_to='customer_photos')
    resume = models.FileField(upload_to='customer_resumes')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    maker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customers', limit_choices_to={'user_type': 'maker'})

class MakerCheckerRelationship(models.Model):
    maker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='makers', limit_choices_to={'user_type': 'maker'})
    checker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='checkers', limit_choices_to={'user_type': 'checker'})