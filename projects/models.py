from django.db import models
from accounts.models import User


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tags = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    preview_url = models.URLField()
    file_url = models.FileField(upload_to='projects/')
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved')], default='pending')
    
    
class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
class WishlistRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    stack = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved')], default='pending')


