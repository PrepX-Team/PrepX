from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy

from .forms import StudentRegisterForm, TeacherRegisterForm, ProfileEditForm
from .decorators import role_required
from .models import User
from subjects.models import Subject, Topic
from questions.models import Question


# ---------- Registration ----------

def register_student(request):
    form = StudentRegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(
            request,
            "Account created successfully. Please log in."
        )
        return redirect('login')

    return render(
        request,
        'accounts/student_register.html',
        {'form': form}
    )


def register_teacher(request):
    form = TeacherRegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(
            request,
            "Registration successful. Your account is awaiting administrator approval."
        )
        return redirect('login')

    return render(
        request,
        'accounts/teacher_register.html',
        {'form': form}
    )


# ---------- Login / Logout ----------

def login_view(request):
    if request.user.is_authenticated:
        return redirect('role_redirect')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:
            messages.error(request, "Invalid username or password.")

        elif not user.is_active:
            messages.error(
                request,
                "This account has been deactivated."
            )

        elif user.role == 'teacher' and not user.is_approved:
            messages.warning(
                request,
                "Your teacher account is awaiting administrator approval."
            )

        else:
            login(request, user)
            return redirect('role_redirect')

    return render(request, 'accounts/login.html')


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')


@login_required
def role_redirect(request):
    """Single entry point that sends each role to its own dashboard."""

    role_map = {
        'admin': 'admin_dashboard',
        'teacher': 'teacher_dashboard',
        'student': 'student_dashboard',
    }

    return redirect(
        role_map.get(request.user.role, 'login')
    )


# ---------- Dashboards ----------

@role_required('student')
def student_dashboard(request):
    context = {
        'tests_attempted': 0,
        'average_score': 0,
        'topics_started': 0,
        'certificates_earned': 0,
    }

    return render(
        request,
        'dashboards/student.html',
        context
    )


@role_required('teacher')
def teacher_dashboard(request):
    context = {
        'my_questions': Question.objects.filter(
            created_by=request.user,
            is_active=True
        ).count(),

        'global_questions': Question.objects.filter(
            is_global=True,
            is_active=True
        ).count(),
    }

    return render(
        request,
        'dashboards/teacher.html',
        context
    )


@role_required('admin')
def admin_dashboard(request):
    context = {
        'total_students': User.objects.filter(
            role='student'
        ).count(),

        'total_teachers': User.objects.filter(
            role='teacher'
        ).count(),

        'pending_teachers': User.objects.filter(
            role='teacher',
            is_approved=False
        ).count(),

        'total_subjects': Subject.objects.filter(
            is_active=True
        ).count(),

        'total_topics': Topic.objects.filter(
            is_active=True
        ).count(),

        'total_questions': Question.objects.filter(
            is_active=True
        ).count(),

        'global_questions': Question.objects.filter(
            is_global=True,
            is_active=True
        ).count(),
    }

    return render(
        request,
        'dashboards/admin.html',
        context
    )


# ---------- Teacher approval ----------

@role_required('admin')
def pending_teachers(request):
    teachers = User.objects.filter(
        role='teacher',
        is_approved=False,
        is_active = True
    )

    return render(
        request,
        'accounts/pending_teachers.html',
        {'teachers': teachers}
    )


@role_required('admin')
@require_POST
def approve_teacher(request, pk):
    teacher = get_object_or_404(
        User,
        pk=pk,
        role='teacher'
    )

    teacher.is_approved = True
    teacher.save()

    messages.success(
        request,
        f"{teacher.username} has been approved."
    )

    return redirect('pending_teachers')


@role_required('admin')
@require_POST
def reject_teacher(request, pk):
    teacher = get_object_or_404(
        User,
        pk=pk,
        role='teacher'
    )

    teacher.is_active = False
    teacher.save()

    messages.info(
        request,
        f"{teacher.username}'s registration was rejected."
    )

    return redirect('pending_teachers')


# ---------- Profile ----------

@login_required
def profile_view(request):
    return render(
        request,
        'accounts/profile.html',
        {'profile_user': request.user}
    )


@login_required
def edit_profile(request):
    form = ProfileEditForm(
        request.POST or None,
        instance=request.user
    )

    if request.method == 'POST' and form.is_valid():
        form.save()

        messages.success(
            request,
            "Profile updated successfully."
        )

        return redirect('profile')

    return render(
        request,
        'accounts/edit_profile.html',
        {'form': form}
    )


# ---------- Custom error handlers ----------

def custom_403(request, exception=None):
    return render(
        request,
        '403.html',
        status=403
    )


def custom_404(request, exception=None):
    return render(
        request,
        '404.html',
        status=404
    )


def custom_500(request):
    return render(
        request,
        '500.html',
        status=500
    )