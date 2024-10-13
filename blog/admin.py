from django.contrib import admin

from .forms import PostForm
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'featured')
    list_filter = ('category', 'featured')
    search_fields = ('title', 'content')
    form = PostForm  # If you have a custom form

admin.site.register(Post, PostAdmin)
admin.site.register(Category)


from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'email', 'profile_picture']

# from django.contrib import admin
# from .models import Post
# from .forms import PostForm  # Import PostForm directly, avoid circular import issues

# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     form = PostForm