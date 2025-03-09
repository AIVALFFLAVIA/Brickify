from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .forms import RegisterForm, LoginForm
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(f"User saved: {user.username}, Role: {user.role}")

            # Get selected role
            role = form.cleaned_data.get('role')
            print(f" Selected Role: {role}")

            # Assign user to correct role
            if role == 'company_leader':
                group, _ = Group.objects.get_or_create(name="Company Leaders")
                user.groups.add(group)
                user.is_staff = False  # Ensure leaders are not admins
                user.is_superuser = False
                user.save()

                print(f" User as leader saved: {user.username}")
                redirect_url = 'management:leader_dashboard'  # Ensure the URL name is correct

            elif role == 'admin':
                user.is_superuser = True  # Make admin
                user.is_staff = True  # Allow access to Django admin
                user.save()

                print(f" User as admin saved: {user.username}")
                redirect_url = '/admin/'  # Redirect to admin panel

            login(request, user)  # Auto-login after registration

            print(f" Redirecting to: {redirect_url}")
            return redirect(redirect_url)
        else:
            print(" Form errors:", form.errors)

    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                print(f"Redirecting user to: {user}")
                return redirect_user_based_on_role(user)  # Redirect based on role
            else:
                # If authentication fails, show an error message
                messages.error(request, 'Invalid username or password.')

    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('dashboard')  # Redirect to dashboard after logout

# Function to Redirect Users Based on Role
def redirect_user_based_on_role(user):
    if user.is_superuser:  # Check if the user is a superuser (admin)
        return redirect('/admin/')  # Admins go to Django Admin Panel
    elif user.groups.filter(name='Company Leaders').exists():  # Custom logic for company leaders
        return redirect('management:leader_dashboard')  # Leaders go to their dashboard
    return redirect('dashboard')  # Default redirect (read-only dashboard)
