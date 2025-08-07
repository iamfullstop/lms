
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User 
# from .forms import UserEditForm
from django.contrib.auth import authenticate

def register_view(request):
    if request.method == "POST":
        full_name = request.POST.get('fullname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            full_name=full_name
        )
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin')
            elif user.role == 'instructor':
                return redirect('instructor_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            messages.error(request, "Invalid credentials.")
        return redirect('login')

    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def student_dashboard(request):
    return render(request, 'home/student_dashboard.html')

@login_required
def instructor_dashboard(request):
    return render(request, 'home/instructor_dashboard.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if current password is correct
        if not request.user.check_password(current_password):
            messages.error(request, 'Your current password is incorrect.')
            return redirect('change_password')

        # Check if new passwords match
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('change_password')

        # Change the password
        request.user.set_password(new_password)
        request.user.save()

        # Keep user logged in after password change
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Your password was updated successfully.')
        return redirect('home')  # Or redirect wherever appropriate

    return render(request, 'home/change_password.html')

# @login_required
# def profile(request):
#     user = request.user
#     if request.method == 'POST':
#         print("FILES:", request.FILES)  # ✅ Debugging line
#         form = UserEditForm(request.POST, request.FILES, instance=user)

#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Profile updated successfully.')
#             return redirect('profile')  
#         else:
#             messages.error(request, 'Please correct the errors below.')

#     else:
#         form = UserEditForm(instance=user)

#     return render(request, 'home/edit_profile.html', {
#         'form': form,
#         'user': user,  # ✅ needed for displaying current profile pic
#     })