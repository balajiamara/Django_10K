from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator


# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=25, 
                          validators=[MinLengthValidator(20),
                                      RegexValidator(
                                          regex=r'^[A-Za-z]+$',
                                          message='Name must contain alphabets only'
                                      )])
    email=models.CharField(max_length=30)
    mobile=models.CharField(max_length=10,
                            validators=[
                                RegexValidator(
                                    regex=r'^[9876]\d{9}$',
                                    message='Mobile number must start with 9,8,7,6'
                                )
                            ])
    imgg=models.FileField(upload_to="profile/")