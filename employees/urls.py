from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import api
from . import views
from jwtauth import views as jwtauth_views


router = DefaultRouter()

router.register(r'departments', api.DepartmentViewSet)
router.register(r'employees', api.EmployeeViewSet)
router.register(r'addresses', api.AddressViewSet)
router.register(r'salaries', api.SalaryViewSet)
router.register(r'attendance', api.AttendanceViewSet)
router.register(r'leave-requests', api.LeaveRequestViewSet)
router.register(r'position-hierarchy', api.PositionHierarchyViewSet)

urlpatterns = [
    path('', views.main_page, name='main_page'),

    path('signup/', views.signup_form, name='signup'),
    path('login/', views.login_form, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path("employees/", views.employee_form, name="employee_form"),
    path('departments/', views.department_form, name='department_form'),
    path('address/', views.address_form, name='address_form'),
    path('salaries/', views.salary_form, name='salary_form'),
    path('attendence/', views.attendence_form, name='attendence_form'),
    path('leave-requests/', views.leave_request_form, name='leave_request_form'),
    path('position-hierarchy/', views.position_hierarchy_form,
         name='position_hierarchy'),


    path('api/', include(router.urls)),
]
