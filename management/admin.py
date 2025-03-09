from django.contrib import admin
from .models import Company, Client, Project, Employee, Supplier, Material, Equipment, FinancialTransaction, Task

admin.site.register(Company)
admin.site.register(Client)
admin.site.register(Project)
admin.site.register(Employee)
admin.site.register(Supplier)
admin.site.register(Material)
admin.site.register(Equipment)
admin.site.register(FinancialTransaction)
admin.site.register(Task)