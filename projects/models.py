from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Project(models.Model):
    title = models.CharField(max_length=100)
    short_description = models.TextField()
    full_description = models.TextField()
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    project_type = models.CharField(max_length=10, choices=[("Free", "Free"), ("Paid", "Paid")])
    tags = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    zip_file = models.FileField(upload_to='zips/', null=True, blank=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")], default="pending")
    is_featured = models.BooleanField(default=False)
    total_downloads = models.IntegerField(default=0)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
