from datetime import datetime 
from django.db import models

# Create your models here.
class Member(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    pw = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    tel = models.CharField(max_length=20)
    birth = models.DateField(blank=True)
    gender = models.CharField(max_length=10)
    email = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=100)
    address1 = models.CharField(max_length=300)
    address2 = models.CharField(max_length=200)
    hobby = models.CharField(max_length=50)
    reg_date = models.DateTimeField(default=datetime.now(),blank=True)
    
    def __str__(self):
        return self.id