from django.views.generic import DetailView, CreateView, UpdateView
from django.contrib.auth.forms import AuthenticationForm
from .models import Post, Category
from .forms import PostForm, UserRegisterForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.views import LoginView

# User registration view
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('index')  # Redirect to homepage or another page
    else:
        form = UserRegisterForm()
    
    return render(request, 'blog/register.html', {'form': form})

# Custom login view
class CustomLoginView(LoginView):
    template_name = 'login.html'

# Login view for handling authentication
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('/')
    form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('/')

# Index view to display all posts with pagination
def index(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {'page_obj': page_obj})

# Post detail view
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})

# View to filter posts by category
def category_posts(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    posts = Post.objects.filter(category=category)
    return render(request, 'blog/category_posts.html', {'category': category, 'posts': posts})

# Search posts view
def search_posts(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    context = {
        'posts': posts,
        'query': query,  # Add the query to the context
    }
    return render(request, 'blog/search_results.html', context)

# View to create a new post
@login_required  # Ensure the user is logged in
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, user=request.user)  # Pass the logged-in user to the form
        if form.is_valid():
            post = form.save(commit=False)  # Create the Post object but don't save it to the database yet
            post.author = request.user  # Set the author to the logged-in user
            post.save()  # Now save the Post
            return redirect('post_detail', id=post.id)  # Redirect to the post detail page
    else:
        form = PostForm()  # Create an empty form

    return render(request, 'create_post.html', {'form': form})

# Class-based view for creating posts
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')  # Redirect to a list view after creation

# Class-based view for updating posts
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')  # Redirect after update

# Class-based detail view for posts
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  # Ensure this template exists
    context_object_name = 'post'
