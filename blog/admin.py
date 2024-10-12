

# Register your models here.
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
