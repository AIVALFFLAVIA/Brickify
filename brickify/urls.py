"""
URL configuration for brickify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from management.views import dashboard_view , unauthorized, company_list, project_list, client_list, employee_list, equipment_list, material_list,supplier_list, task_list, financial_transaction_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Include the accounts URLs
    path('dashboard/', dashboard_view, name='dashboard'),
    path('', include('management.urls')), 
    path('unauthorized/', unauthorized, name='unauthorized'),
    path('companies/', company_list, name='company_list'),
    path('clients/', client_list, name='client_list'),
    path('projects/', project_list, name='project_list'),
    path('employees/', employee_list, name='employee_list'),
    path('equipments/', equipment_list, name='equipment_list'),
    path('materials/', material_list, name='material_list'),
    path('suppliers/', supplier_list, name='supplier_list'),
    path('tasks/', task_list, name='task_list'),
    path('financial_transactions/', financial_transaction_list, name='financial_transaction_list'),
]
