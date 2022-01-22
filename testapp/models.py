from django.db import models
import datetime


# Create your models here.
class UserProfile(models.Model):
    customer_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    dob = models.DateField(max_length=8)
    phone=models.CharField(max_length=16,unique = True)
    email=models.EmailField(max_length=100,unique = True)
    password=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    gender_type=(("male","Male"),("female","Female"),("others","Others"))
    gender=models.CharField(default="male",choices=gender_type,max_length=40)
