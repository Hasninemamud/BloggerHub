from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile, Post
from ckeditor.widgets import CKEditorWidget


# User profile form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'address', 'phone', 'profile_picture',]

# Post form
class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), label="Post Content")

    class Meta:
        model = Post
        fields = ['title', 'content',  'category', 'featured', 'image']
        # 'author',

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'border border-gray-300 rounded-lg p-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-600'
            })

        if user is not None:
            self.fields['author'].initial = user  # Set author field to logged-in user
            self.fields['author'].widget.attrs['readonly'] = True  # Make it read-only
