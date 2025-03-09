from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Company Model
class Company(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_email = models.EmailField(unique=True)
    contact_phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

# Client Model
class Client(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.TextField()
    email = models.EmailField(unique=True)
    address = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="clients")

    def __str__(self):
        return self.name

# Project Model
class Project(models.Model):
    STATUS_CHOICES = [
        ('Planning', 'Planning'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    ]
    name = models.CharField(max_length=255)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="projects")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="projects")
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name

# Employee Model
class Employee(models.Model):
    POSITION_CHOICES = [
        ('Engineer', 'Engineer'),
        ('Laborer', 'Laborer'),
        ('Manager', 'Manager')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employees")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Supplier Model
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.TextField()
    email = models.EmailField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="suppliers")

    def __str__(self):
        return self.name

# Material Model
class Material(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="materials")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="materials")

    def __str__(self):
        return self.name

# Equipment Model
class Equipment(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('In Use', 'In Use'),
        ('Maintenance', 'Maintenance')
    ]
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    purchase_date = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="equipment")

    def __str__(self):
        return self.name

# Financial Transaction Model
class FinancialTransaction(models.Model):
    TRANSACTION_CHOICES = [
        ('Expense', 'Expense'),
        ('Payment Received', 'Payment Received')
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_CHOICES)
    date = models.DateField()
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="transactions")

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"

# Task Model
class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    task_name = models.CharField(max_length=255)
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    deadline = models.DateField()

    def __str__(self):
        return self.task_name
