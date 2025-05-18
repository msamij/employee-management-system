from rest_framework import serializers
from .models import *


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class SalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Salary
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = '__all__'


class PositionHierarchySerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionHierarchy
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    salaries = SalarySerializer(many=True, read_only=True)
    attendance_records = AttendanceSerializer(many=True, read_only=True)
    leave_requests = LeaveRequestSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
