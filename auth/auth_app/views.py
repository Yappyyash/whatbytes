from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .middlewares import auth, guest
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages

User = get_user_model()
@guest
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        initial_data={'username':'', 'email':'', 'password1':'', 'password2':''}
        form = CustomUserCreationForm(initial=initial_data)
    return render(request, 'auth/register.html', {'form': form})
@guest
def login_view(request):
    if request.method == 'POST':
        form=AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        initial_data = {'username':'', 'password1':""}
        form=AuthenticationForm(initial=initial_data)
    return render(request, 'auth/login.html', {'form':form})

@auth
def dashboard_view(request):
    return render(request, 'dashboard.html')


@guest
def forgot_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=True,
                email_template_name='auth/password_reset_email.html',
                subject_template_name='auth/password_reset_subject.txt'
            )
            messages.success(request, 'Password reset instructions have been sent to your email.')
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'auth/forgot.html', {'form': form})

@auth
def profile_view(request):
    user = request.user
    context = {
        'username': user.username,
        'email': user.email,
        'date_joined': user.date_joined,
        'last_login': user.last_login
    }
    return render(request, 'auth/profile.html', context)

@auth
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'auth/change_password.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
