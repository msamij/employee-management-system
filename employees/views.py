from django.http import HttpResponseForbidden
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect

from django.contrib import messages


from .models import Employee, Department


def redirect_authenticated_user(request, redirect_route):
    """Redirect authenticated normal users to route provided in redite_route, forbid admins."""
    if request.user.is_superuser or request.user.is_staff:
        return HttpResponseForbidden("Admins are not allowed to access this page.")
    if request.user.is_authenticated:
        return redirect(redirect_route)
    return None


def main_page(request):
    response = redirect_authenticated_user(request, 'employee_form')
    if response:
        return response
    return redirect('signup')


@csrf_protect
def signup_form(request):
    response = redirect_authenticated_user(request, 'employee_form')
    if response:
        return response

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        messages.success(request, 'User logged in successfully.')
        return redirect('employee_form')

    return render(request, 'register/signup.html')


@csrf_protect
def login_form(request):
    response = redirect_authenticated_user(request, 'employee_form')
    if response:
        return response

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('employee_form')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('login')

    return render(request, 'register/login.html')


def logout_user(request):
    logout(request)
    return redirect('main_page')


@csrf_protect
@login_required(login_url='signup')
def employee_form(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        date_of_birth = request.POST.get('date_of_birth')
        hire_date = request.POST.get('hire_date')
        job_title = request.POST.get('job_title')
        status = request.POST.get('status')
        profile_picture = request.FILES.get('profile_picture')

        employee = Employee.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_no,
            date_of_birth=date_of_birth,
            hire_date=hire_date,
            job_title=job_title,
            status=status,
            profile_picture=profile_picture
        )
        return redirect('employee_form')
    return render(request, 'employeeForm.html')


@login_required(login_url='signup')
def department_form(request):
    if request.method == 'POST':
        department_name = request.POST.get('name')
        description = request.POST.get('description')
        manager_id = request.POST.get('manager')

        manager = Employee.objects.get(id=manager_id)
        Department.objects.create(
            name=department_name, description=description, manager=manager)
        return redirect('department_form')

    employees = Employee.objects.all()
    return render(request, 'departmentForm.html', {'employees': employees})
