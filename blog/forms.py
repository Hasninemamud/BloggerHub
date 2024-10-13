from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile, Post
from ckeditor.widgets import CKEditorWidget

# # User registration form
# class UserRegisterForm(forms.ModelForm):
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         if User.objects.filter(username=username).exists():
#             raise ValidationError("Username is already taken.")
#         return username

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if User.objects.filter(email=email).exists():
#             raise ValidationError("Email is already in use.")
#         return email

#     def clean(self):
#         cleaned_data = super().clean()
#         password1 = cleaned_data.get('password1')
#         password2 = cleaned_data.get('password2')

#         if password1 and password2 and password1 != password2:
#             raise ValidationError("Passwords do not match.")
#         return cleaned_data

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
        fields = ['title', 'content', 'author', 'category', 'featured', 'image']

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
