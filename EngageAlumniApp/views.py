from django.contrib.auth import login , logout , authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django.contrib import messages
from .models import StudentProfile, AlumniProfile
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile, Post , JobPost
from .forms import ProfileForm, JobPostForm, PostForm
from django.utils import timezone




# Create your views here.
def index(request):
    # Fetch all job posts
    job_posts = JobPost.objects.all()

    return render(request, 'EngageAluminiApp/index.html', {'job_posts': job_posts})


def learn(request):
    return render(request,'EngageAluminiApp/learn.html')

def events(request):
    return render(request,'EngageAluminiApp/events.html')

def alumninetwork(request):
    return render(request,'EngageAluminiApp/alumninetwork.html')

def alumnidirectory(request):
    return render(request,'EngageAluminiApp/alumnidirectory.html')

def mentor(request):
    return render(request,'EngageAluminiApp/mentor.html')

def john(request):
    return render(request,'EngageAluminiApp/john.html')

def shruti(request):
    return render(request,'EngageAluminiApp/shruti.html')

def rohit(request):
    return render(request,'EngageAluminiApp/rohit.html')

def success_stories(request):
    return render(request,'EngageAluminiApp/success_stories.html')

# Custom Signup View

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        user_type = request.POST.get('user_type')

        # Check if passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'EngageAluminiApp/signup.html')

        # Check if username or email already exists
        if User.objects.filter(Q(username=username) | Q(email=email)).exists():
            messages.error(request, 'Username or email already exists. Please try again.')
            return render(request, 'EngageAluminiApp/signup.html')

        # Create user and save to the database
        user = User.objects.create_user(username=username, password=password1, email=email)

        # Handle student signup
        if user_type == 'student':
            college_user_id = request.POST.get('college_user_id')
            department = request.POST.get('department')

            # Additional validation for student fields
            if not college_user_id or not department:
                messages.error(request, 'Please fill all student details.')
                return render(request, 'EngageAluminiApp/signup.html')

            # Create and save the student profile
            StudentProfile.objects.create(user=user, college_user_id=college_user_id, email=email, department=department)
            messages.success(request, 'Student account created successfully!')
            return redirect('home')

        # Handle alumni signup
        elif user_type == 'alumni':
            name = request.POST.get('name')
            current_position = request.POST.get('current_position')
            marksheet = request.FILES.get('marksheet')

            # Additional validation for alumni fields
            if not name or not current_position or not marksheet:
                messages.error(request, 'Please fill all alumni details and upload the marksheet.')
                return render(request, 'EngageAluminiApp/signup.html')

            # Create and save the alumni profile
            AlumniProfile.objects.create(user=user, name=name, current_position=current_position, marksheet=marksheet)
            messages.success(request, 'Alumni account created successfully!')
            return redirect('home')

        else:
            messages.error(request, 'Invalid user type selected.')
            return render(request, 'EngageAluminiApp/signup.html')

    return render(request, 'EngageAluminiApp/signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home or any other page
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'EngageAluminiApp/login.html')

def custom_logout_view(request):
    logout(request)
    return redirect('/')


def search(request):
    query = request.GET.get('q')
    if query:
        results = User.objects.filter(username__icontains=query)
    else:
        results = User.objects.none()
    
    return render(request, 'EngageAluminiApp/search_results.html', {'results': results})




@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'EngageAluminiApp/profile.html', {'form': form})

# View for posting jobs
@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job_post = form.save(commit=False)
            job_post.user = request.user
            job_post.save()
            return redirect('job_list')
    else:
        form = JobPostForm()
    return render(request, 'EngageAluminiApp/job_posting.html', {'form': form})

# View for sharing posts/projects
@login_required
def share_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'EngageAlumniniApp/share_post.html', {'form': form})

# Job list view (to display all jobs)
def job_list(request):
    jobs = JobPost.objects.all().order_by('-posted_at')
    return render(request, 'job_list.html', {'jobs': jobs})

# Post list view (to display all shared posts)
def post_list(request):
    posts = Post.objects.all().order_by('-posted_at')
    return render(request, 'post_list.html', {'posts': posts})


@login_required

@login_required
def job_posting(request):
    if request.method == 'POST':
        # Retrieve form data from the request
        job_title = request.POST.get('job_title')
        company_name = request.POST.get('company_name')  # Not used in the model, but available
        job_description = request.POST.get('job_description')
        location = request.POST.get('location')

        # Create and save a new JobPost instance
        job_post = JobPost(
            user=request.user,
            title=job_title,
            description=job_description,
            location=location,
            posted_at=timezone.now()  # Use current time for posting
        )
        job_post.save()

        return redirect('profile')  # Redirect to a success page or profile

    return render(request, 'EngageAluminiApp/job_posting.html')


def apply_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    # Handle job application logic here
    return render(request, 'EngageAluminiApp/apply_job.html', {'job': job})

def upload_resume(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    if request.method == 'POST':
        # Handle resume upload logic here
        return redirect('index')  # Redirect after successful upload