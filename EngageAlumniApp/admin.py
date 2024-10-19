from django.contrib import admin
from .models import StudentProfile, AlumniProfile
from .models import JobPost

# Register your models here.
admin.site.register(StudentProfile)
admin.site.register(AlumniProfile)


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'location', 'posted_at')
    search_fields = ('title', 'description', 'location')

