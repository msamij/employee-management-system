from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import api
from . import views


router = DefaultRouter()

router.register(r'departments', api.DepartmentViewSet)
router.register(r'employees', api.EmployeeViewSet)
router.register(r'addresses', api.AddressViewSet)
router.register(r'salaries', api.SalaryViewSet)
router.register(r'attendance', api.AttendanceViewSet)
router.register(r'leave-requests', api.LeaveRequestViewSet)
router.register(r'position-hierarchy', api.PositionHierarchyViewSet)

urlpatterns = [
    path("employees/", views.employee_form, name="employee_form"),
    path('departments/', views.department_form, name='department_form'),
    path('api/', include(router.urls)),
]
