from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_approved:
                messages.error(request, "Your teacher account is pending admin approval.")
                return render(request, 'accounts/login.html')
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})
