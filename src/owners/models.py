from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    opening_hour = models.TimeField()
    closing_hour = models.TimeField()