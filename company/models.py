from django.db import models

# Create your models here.
class CompanyGroup(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta():
        db_table = "company_groups"


class Company(models.Model):
    company_group = models.ForeignKey(CompanyGroup, on_delete=models.CASCADE, null=True)
    name  = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta():
        db_table = "companies"


class Representative(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=254, null=True)
    
    def __str__(self):
        return self.name

    class Meta():
        db_table = "representatives"