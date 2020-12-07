from django.db import models

from company.models import Company, Representative
from employee.models import Employee
# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100, null=True)
    category_content = models.CharField(max_length=100, null=True)
    
    class Meta():
        db_table = 'categories'


class Process(models.Model):
    title = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    class Meta():
        db_table = "processes"


class Contract(models.Model):
    category = models.ManyToManyField('Category', through='ContractCategory')
    process = models.ManyToManyField('Process', through='ContractProcess')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    representative = models.ForeignKey(Representative, on_delete=models.CASCADE, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    memo = models.TextField(null=True)


    class Meta():
        db_table = "contracts"

class ContractCategory(models.Model):
    target_contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta():
        db_table = 'contract_categories'

class ContractProcess(models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE, null=True)
    target_contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    revenue = models.DecimalField(max_digits=14, decimal_places=2, null = True)
    vat = models.DecimalField(max_digits=12, decimal_places=2, null = True)
    issue_date = models.DateField(auto_now=False, auto_now_add=False, null=True)

    class Meta():
        db_table = "contract_processes"
