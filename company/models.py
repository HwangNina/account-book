from django.db import models

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta():
        db_table = "groups"


class Company(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    name  = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta():
        db_table = "companies"


class Representative(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    
    def __str__(self):
        return self.name

    class Meta():
        db_table = "representatives"