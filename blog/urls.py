from django import views
from django.urls import path

from myblog import settings
from .  import views
# from .views import register
from django.contrib.auth import views as auth_views
# from .views import CustomLoginView
from .views import PostDetailView, PostCreateView, PostUpdateView
from .views import profile_view, edit_profile_view, register, login_view, logout_view, index
from django.conf.urls.static import static
# from .views import UserProfileView
urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),  # Detail view URL
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('category/<int:category_id>/', views.category_posts, name='category_posts'),
    path('search/', views.search_posts, name='search_posts'),
    path('create_post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('user/<int:id>/', views.profile_view, name='user_profile'),  
    path('profile/', views.profile_view, name='profile'),
    path('profile/user/<int:id>/', views.edit_profile_view, name='edit_profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),  
    path('logout/', views.logout_view, name='logout_view'),
    path('', views.index, name='index'),
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
