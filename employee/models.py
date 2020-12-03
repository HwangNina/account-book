from django.db import models

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=50)
    account = models.CharField(max_length=50)
    password = models.CharField(max_length=300)
    is_admin = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta():
        db_table = "employees"