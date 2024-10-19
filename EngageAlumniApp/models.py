from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college_user_id = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user.username} - Student'

class AlumniProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    current_position = models.CharField(max_length=200)
    marksheet = models.FileField(upload_to='marksheets/')

    def __str__(self):
        return f'{self.user.username} - Alumni'
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    github_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

# Job Post model
class JobPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,default='')
    description = models.TextField(default='')
    location = models.CharField(max_length=100, blank=True, null=True)
    posted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

# Shared Post/Project model
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,default='')
    description = models.TextField(default='')
    posted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

