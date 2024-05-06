from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    opening_hour = models.TimeField()
    closing_hour = models.TimeField()

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    birth_date = models.DateField()
    last_name = models.CharField(max_length=100)
    dni = models.CharField(max_length=8)
    branch_name = models.CharField(max_length=100)