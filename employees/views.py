from django.shortcuts import render, redirect
from .models import Employee, Department


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
    return render(request, 'department_form.html', {'employees': employees})
