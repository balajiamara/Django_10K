from django.db import models

# Create your models here.
class Check(models.Model):
    userid=models.IntegerField(primary_key=True)
    username=models.CharField(unique=True,max_length=25)
    password=models.CharField(max_length=25)