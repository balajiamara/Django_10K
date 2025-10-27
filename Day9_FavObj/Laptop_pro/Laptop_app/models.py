from django.db import models

# Create your models here.
class Laptop(models.Model):
    lap_id=models.IntegerField(primary_key=True)
    lap_brand=models.CharField(max_length=10)
    lap_specs=models.CharField(max_length=20)
    lap_price=models.CharField(max_length=10)