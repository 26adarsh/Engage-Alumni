from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import signup ,custom_logout_view
from .views import user_login , search
from .views import apply_job, upload_resume


urlpatterns = [
    path('', views.index,name='home'),
    path('learn/',views.learn,name='learn'),
    path('events',views.events,name='events'),
    path('alumninetwork',views.alumninetwork,name='alumninetwork'),
    path('alumnidirectory',views.alumnidirectory,name='alumnidirectory'),
    path('login/', auth_views.LoginView.as_view(template_name='EngageAluminiApp/login.html'), name='login'),
    path('logout/', custom_logout_view, name='logout'),
    path('mentor/',views.mentor,name='mentor'),
    path('john/',views.john,name='john'),
    path('shurti/',views.shruti,name='shruti'),
    path('rohit/',views.rohit,name='rohit'),
    path('success_stories/',views.success_stories,name='success_stories'),

    # Signup URL
    path('signup/', views.signup, name='signup'),
    path('search/', search, name='search'),
    path('profile/', views.profile_view, name='profile'),
    path('job_posting/', views.job_posting, name='job_posting'),
    path('share_post/', views.share_post, name='share_post'),
    path('jobs/', views.job_list, name='job_list'),
    path('posts/', views.post_list, name='post_list'),
    
    path('apply/<int:job_id>/', apply_job, name='apply_job'),
    path('upload_resume/<int:job_id>/', upload_resume, name='upload_resume'),
    
    
]


