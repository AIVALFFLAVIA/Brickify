from django.urls import path
from . import views 
from .views import dashboard_view
app_name = 'management' 

urlpatterns = [

    path('', dashboard_view, name='dashboard'),
    path('leader-dashboard/', views.leader_dashboard, name='leader_dashboard'),

    path('unauthorized/', views.unauthorized, name='unauthorized'),

    # Company URLs
    path('companies/', views.company_list, name='company_list'),
    path('company/create/', views.company_create, name='company_create'),
    path('company/update/<int:id>/', views.company_update, name='company_update'),
    path('company/delete/<int:id>/', views.company_delete, name='company_delete'),

    # Client URLs
    path('clients/', views.client_list, name='client_list'),
    path('client/create/', views.client_create, name='client_create'),
    path('client/update/<int:id>/', views.client_update, name='client_update'),
    path('client/delete/<int:id>/', views.client_delete, name='client_delete'),

    # Project URLs
    path('projects/', views.project_list, name='project_list'), 
    path('project/create/', views.project_create, name='project_create'),
    path('project/update/<int:id>/', views.project_update, name='project_update'),
    path('project/delete/<int:id>/', views.project_delete, name='project_delete'),

    # Employee URLs
    path('employees/', views.employee_list, name='employee_list'),
    path('employee/create/', views.employee_create, name='employee_create'),
    path('employee/update/<int:id>/', views.employee_update, name='employee_update'),
    path('employee/delete/<int:id>/', views.employee_delete, name='employee_delete'),

    # Supplier URLs
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('supplier/create/', views.supplier_create, name='supplier_create'),
    path('supplier/update/<int:id>/', views.supplier_update, name='supplier_update'),
    path('supplier/delete/<int:id>/', views.supplier_delete, name='supplier_delete'),

    # Material URLs
    path('materials/', views.material_list, name='material_list'),
    path('material/create/', views.material_create, name='material_create'),
    path('material/update/<int:id>/', views.material_update, name='material_update'),
    path('material/delete/<int:id>/', views.material_delete, name='material_delete'),

    # Equipment URLs
    path('equipments/', views.equipment_list, name='equipment_list'),
    path('equipment/create/', views.equipment_create, name='equipment_create'),
    path('equipment/update/<int:id>/', views.equipment_update, name='equipment_update'),
    path('equipment/delete/<int:id>/', views.equipment_delete, name='equipment_delete'),

    # Financial Transaction URLs
    path('financial_transactions/', views.financial_transaction_list, name='financial_transaction_list'),
    path('financial_transaction/create/', views.financial_transaction_create, name='financial_transaction_create'),
    path('financial_transaction/update/<int:id>/', views.financial_transaction_update, name='financial_transaction_update'),
    path('financial_transaction/delete/<int:id>/', views.financial_transaction_delete, name='financial_transaction_delete'),

    # Task URLs
    path('tasks/', views.task_list, name='task_list'),
    path('task/create/', views.task_create, name='task_create'),
    path('task/update/<int:id>/', views.task_update, name='task_update'),
    path('task/delete/<int:id>/', views.task_delete, name='task_delete'),

  
]
