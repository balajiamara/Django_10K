from django.db import models

# Create your models here.
class Insta_Acc(models.Model):
    userid=models.IntegerField(primary_key=True)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    profile_pic=models.URLField()
    # profile_pic=models.FileField(upload_to="profile/")