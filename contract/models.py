from django.db import models

from company.models import Company, Representative
from employee.models import Employee
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta():
        db_table = "categories"


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta():
        db_table = "subcategories"


class Process(models.Model):
    process = models.CharField(max_length=50)

    def __str__(self):
        return self.process

    class Meta():
        db_table = "processes"


class ProcessStatus(models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.status

    class Meta():
        db_table = "statuses"


class Contract(models.Model):
    status = models.ForeignKey(ProcessStatus, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    category_content = models.CharField(max_length=500, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    representative = models.ForeignKey(Representative, on_delete=models.CASCADE, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    revenue = models.DecimalField(max_digits=14, decimal_places=2, null=True)
    issue_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    memo = models.TextField(null=True)

    class Meta():
        db_table = "contracts"
