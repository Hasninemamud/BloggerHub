from django.views.generic import DetailView, CreateView, UpdateView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Post, Category, UserProfile
from .forms import PostForm, UserProfileForm
from django.contrib.auth.models import User  # Make sure this line is included




@login_required
def edit_profile_view(request, id):
    # Fetch the user profile for the logged-in user
    profile = get_object_or_404(UserProfile, user_id=id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)  # Initialize form with submitted data
        if form.is_valid():
            form.save()  # Save the updated profile
            messages.success(request, "Profile updated successfully!")  # Success message
            return redirect('profile')  # Redirect to the profile page
        else:
            # Debugging: print form errors to console
            print(form.errors)  # This line will help you see what went wrong
    else:
        form = UserProfileForm(instance=profile)  # Initialize form with current profile data

    # Always return the form in the context
    return render(request, 'blog/edit_profile.html', {'form': form})



# User Registration View
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        # Basic validation (server-side)
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'blog/register.html')

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return render(request, 'blog/register.html')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken!")
            return render(request, 'blog/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return render(request, 'blog/register.html')

        # Create new user
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Log in the new user
        login(request, user)  # Ensure user is successfully created before login
        messages.success(request, "Registration successful!")
        return redirect('index')  # Redirect to homepage or success page
    
    return render(request, 'blog/register.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Redirect logged-in users away from login/register views
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})


    # registration logic here as defined


def logout_view(request):
    logout(request)
    return redirect('login_view')

# Index view with pagination for all posts
def index(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)  # Paginate 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {'page_obj': page_obj})

# Post detail view
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})

# Filter posts by category
def category_posts(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    posts = Post.objects.filter(category=category)
    return render(request, 'blog/category_posts.html', {'category': category, 'posts': posts})

# Search posts view
def search_posts(request):
    query = request.GET.get('q')  # Get the search query from the URL
    posts = Post.objects.none()  # Default to no posts
    
    if query:  # Check if there is a query
        posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))

    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})

# Create post view (with user handling)
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Handle form submission
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the logged-in user as the author
            post.save()  # Save the post
            messages.success(request, "Post created successfully!")
            return redirect('post_detail', post_id=post.id)  # Redirect to the post detail page
        else:
            print(form.errors)  # Debugging: print form errors
    else:
        form = PostForm()  # Initialize empty form for GET request

    return render(request, 'blog/create_post.html', {'form': form})  # Render the form



# Class-based views for creating and updating posts
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')  # Redirect to post list view after creation

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')  # Redirect to post list view after update

# Class-based post detail view
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .models import UserProfile, Post
from django.core.paginator import Paginator

@login_required
def user_profile_view(request, id):
    user = get_object_or_404(User, id=id)

    # Check if a UserProfile exists, if not, create one
    profile, created = UserProfile.objects.get_or_create(user=user)

    # Fetch posts authored by this user
    user_posts = Post.objects.filter(author=user)

    # Pagination setup
    paginator = Paginator(user_posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    return render(request, 'blog/profile.html', {
        'profile': profile,
        'user_posts': page_posts,
    })

