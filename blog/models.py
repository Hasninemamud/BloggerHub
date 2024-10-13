from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default.jpg')  # Default image if none is uploaded
    
    def __str__(self):
        return self.user.username

    



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensure unique category names

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')  # Use related_name for better access
    content = RichTextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')  # Use related_name for better access
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)  # Optional image field

    def __str__(self):
        return self.title

