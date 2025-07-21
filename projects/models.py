from django.db import models
from accounts.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

CATEGORY_CHOICES = [
    ('Web Development', 'Web Development'),
    ('Android', 'Android'),
    ('Machine Learning', 'Machine Learning'),
    ('IoT', 'IoT'),
    ('Data Science', 'Data Science'),
    ('Cyber Security', 'Cyber Security'),
    ('Others', 'Others'),
]

PROJECT_TYPE_CHOICES = [
    ('Free', 'Free'),
    ('Paid', 'Paid'),
]

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

class Project(models.Model):            # Core Fields for project info
   
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=255)
    full_description = models.TextField(
    default="This is a default full description"  # ✅ optional if you're not renaming
)
    category = models.CharField(
    choices=CATEGORY_CHOICES,
    max_length=50,
    default="Web Development")
    tech_stack = models.JSONField()  # list of tags
    tools = models.JSONField()       # list of tools/frameworks
    project_type = models.CharField(choices=PROJECT_TYPE_CHOICES, max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tags = models.CharField(max_length=255, blank=True)
    is_edit_pending = models.BooleanField(default=False)
    pending_edits = models.JSONField(null=True, blank=True)

   
   
   # media info
    thumbnail = models.TextField(max_length=500, null=True, blank=True)          
    gallery_images = models.JSONField()  # list of image URLs
    setup_video_url = models.URLField(blank=True, null=True)
    live_demo_url = models.URLField(blank=True, null=True)
    project_zip = models.URLField(max_length=500, null=True, blank=True)
    documentation = models.URLField(max_length=500, null=True, blank=True)



    # System & Metadata
    upload_date = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    total_downloads = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    
    
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
    
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='wishlisted_by')
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.email} - {self.project.title}"


