from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Department(TimeStampedModel):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)
    manager = models.ForeignKey(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_departments'
    )

    def __str__(self):
        return self.name


class Employee(TimeStampedModel):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('On Leave', 'On Leave'),
        ('Terminated', 'Terminated'),
        ('Resigned', 'Resigned'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    hire_date = models.DateField(default=timezone.now)
    job_title = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Active')
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees'
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"First name: {self.first_name}, Last name: {self.last_name}, Email: {self.email}"


class Address(TimeStampedModel):
    ADDRESS_TYPE_CHOICES = [
        ('Home', 'Home'),
        ('Office', 'Office'),
        ('Other', 'Other'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='addresses'
    )
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    address_type = models.CharField(
        max_length=20, choices=ADDRESS_TYPE_CHOICES, default='Home')

    def __str__(self):
        return f"{self.address_type} - {self.employee}"


class Salary(TimeStampedModel):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='salaries'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='PKR')
    effective_from = models.DateField()

    def __str__(self):
        return f"{self.employee} - {self.amount} {self.currency}"


class Attendance(TimeStampedModel):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Leave', 'Leave'),
        ('Half Day', 'Half Day'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    date = models.DateField()
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Present')

    def __str__(self):
        return f"{self.employee} - {self.date} - {self.status}"


class LeaveRequest(TimeStampedModel):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='leave_requests'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.employee} leave ({self.start_date} - {self.end_date})"


class PositionHierarchy(TimeStampedModel):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='subordinates'
    )
    reports_to = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='supervisors'
    )

    def __str__(self):
        return f"{self.employee} reports to {self.reports_to}"
