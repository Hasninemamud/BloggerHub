from django.urls import path
from .  import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView
from .views import PostDetailView, PostCreateView, PostUpdateView

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),  # Detail view URL
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('category/<int:category_id>/', views.category_posts, name='category_posts'),
    path('search/', views.search_posts, name='search_posts'),
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
