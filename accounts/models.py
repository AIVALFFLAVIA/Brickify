from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('company_leader', 'Company Leader'),
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='company_leader')

    def is_admin(self):
        return self.role == 'admin'

    def is_company_leader(self):
        return self.role == 'company_leader'
