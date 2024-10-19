from django import forms
from .models import Profile, JobPost, Post

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_image', 'linkedin_url', 'github_url']

class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = ['title', 'description', 'location']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description']
