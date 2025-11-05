from django.db import models

# Create your models here.


class Menu(models.Model):
    DishId=models.IntegerField(primary_key=True)
    DishName=models.CharField(max_length=50)
    Ingredients=models.TextField()
    Price=models.FloatField()
    Image=models.FileField(upload_to="profile/")