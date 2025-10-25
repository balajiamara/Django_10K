from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User


# Create your views here.
def validate_file(file_obj):
    max_size= 4*1024*1024
    if file_obj.size > max_size:
        return False, 'File is too large. Max size is 4MB.'
    
    alllowed_type=['image/jpeg', 'image/png']
    if file_obj.content_type not in alllowed_type:
        return False, 'Invalid File type. Allowed: JPG, PNG only'
    
    return True, 'Valid File'

@csrf_exempt
def reg_user(req):
    user_name=req.POST.get("name")
    user_email=req.POST.get("email")
    user_mob=req.POST.get("mobile")
    file_obj=req.FILES["imgg"]


    is_valid_file, msg=validate_file(file_obj)

    if is_valid_file:
        pass
    else:
        return HttpResponse(msg)
    

    new_user= User.objects.create(name=user_name, email=user_email, mobile=user_mob, imgg=file_obj)
    return HttpResponse('reg!')