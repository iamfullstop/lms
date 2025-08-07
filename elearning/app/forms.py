from django import forms
from .models import User

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'username', 'bio', 'profile_pic']

