from django.db import models

# Create your models here.



class Company(models.Model):

    class Type(models.TextChoices):
        MNC='M', 'MNC'
        Startup='S', 'Startup'


    name=models.CharField(max_length=10)
    email=models.EmailField()
    capital=models.IntegerField()
    type=models.CharField(
        max_length=1,
        choices=Type.choices,
        default=Type.Startup
    )
    start_date=models.DateField()