from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the custom user model dynamically

class RegisterForm(UserCreationForm):
    ROLE_CHOICES = [
        ('company_leader', 'Company Leader'),
        ('admin', 'Admin')
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User  # Use custom user model
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']  # Set role
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
