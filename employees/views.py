from django.http import HttpResponseForbidden
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

from .models import *


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


@csrf_protect
@login_required(login_url='signup')
def department_form(request):
    if request.method == 'POST':
        department_name = request.POST.get('name')
        description = request.POST.get('description')
        manager_id = request.POST.get('manager')

        manager = None
        if manager_id:
            try:
                manager = Employee.objects.get(id=manager_id)
            except Employee.DoesNotExist:
                manager = None

        Department.objects.create(
            name=department_name, description=description, manager=manager)

        return redirect('department_form')

    employees = Employee.objects.all()
    return render(request, 'departmentForm.html', {'employees': employees})


@csrf_protect
@login_required(login_url='signup')
def address_form(request):
    if request.method == 'POST':
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zipcode = request.POST.get('zipcode')
        address_type = request.POST.get('address_type')
        employee_id = request.POST.get('employee')

        employee = Employee.objects.get(id=employee_id)

        Address.objects.create(employee=employee, street=street, city=city,
                               state=state, country=country, zip_code=zipcode,
                               address_type=address_type)
        return redirect('address_form')

    employees = Employee.objects.all()
    return render(request, 'addressForm.html', {'employees': employees})


@csrf_protect
@login_required(login_url='signup')
def salary_form(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        currency = request.POST.get('currency')
        effective_from = request.POST.get('effective_from')
        employee_id = request.POST.get('employee')

        employee = Employee.objects.get(id=employee_id)

        Salary.objects.create(employee=employee, amount=amount,
                              currency=currency, effective_from=effective_from)
        return redirect('salary_form')

    employees = Employee.objects.all()
    return render(request, 'salaryForm.html', {'employees': employees})


@csrf_protect
@login_required(login_url='signup')
def attendence_form(request):
    if request.method == 'POST':
        date = request.POST.get('get')
        check_in_time = request.POST.get('check_in_time')
        check_out_time = request.POST.get('check_out_time')
        status = request.POST.get('status')
        employee_id = request.POST.get('employee')

        employee = Employee.objects.get(id=employee_id)
        Attendance.objects.create(employee=employee, date=date,
                                  check_in_time=check_in_time, check_out_time=check_out_time,
                                  status=status)
        return redirect('attendence_form')

    employees = Employee.objects.all()
    return render(request, 'attendenceForm.html', {'employees': employees})


@csrf_protect
@login_required(login_url='signup')
def leave_request_form(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')
        status = request.POST.get('status')
        employee_id = request.POST.get('employee')

        employee = Employee.objects.get(id=employee_id)
        LeaveRequest.objects.create(employee=employee, start_date=start_date,
                                    end_date=end_date, reason=reason, status=status)

        return redirect('leave_request_form')

    employees = Employee.objects.all()
    return render(request, 'leaveForm.html', {'employees': employees})


@csrf_protect
@login_required(login_url='signup')
def position_hierarchy_form(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        reports_to = request.POST.get('reports_to')

        employee = Employee.objects.get(id=employee_id)
        employee_manager = Employee.objects.get(id=reports_to)
        PositionHierarchy.objects.create(
            employee=employee, reports_to=employee_manager)

        return redirect('position_hierarchy')

    employees = Employee.objects.all()
    return render(request, 'positionHierarchyForm.html', {'employees': employees})
