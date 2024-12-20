from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)  # e.g., "10 hours"
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='courses/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Instructors(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField()
    expertise = models.CharField(max_length=200)
    image = models.ImageField(upload_to='instructors/', null=True, blank=True)  # For profile picture
    joined_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
def get_default_user():
    # Return an existing user, such as the first one or a specific one
    return CustomUser.objects.first()  # Or select a specific user


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Banner(models.Model):
    title = models.CharField(max_length=255, help_text="Main banner title")
    subtitle = models.CharField(max_length=255, blank=True, null=True, help_text="Optional subtitle for the banner")
    image = models.ImageField(upload_to='banners/', help_text="Upload a banner image")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Payment(models.Model):
    stripe_payment_id = models.CharField(max_length=255, unique=True)  # Stripe Payment ID
    customer_email = models.EmailField()  # Customer email
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Payment amount
    currency = models.CharField(max_length=10, default="USD")  # Payment currency
    status = models.CharField(max_length=50, default="Success")  # Payment status
    created_at = models.DateTimeField(auto_now_add=True)  # Payment date

    def __str__(self):
        return f"{self.customer_email} - {self.amount} {self.currency} - {self.status}"