from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from .models import User


# Create your views here.
#validation of file
def validate_file(file_obj):
    max_size= 4*1024*1024
    if file_obj.size > max_size:
        return False, 'File is too large. Max size is 4MB.'
    
    alllowed_type=['image/jpeg', 'image/png']
    if file_obj.content_type not in alllowed_type:
        return False, 'Invalid File type. Allowed: JPG, PNG only'
    
    return True, 'Valid File'


def get_user(req):
    all_users= User.objects.all()
    dict_dat=all_users.values()
    list_data=list(dict_dat)
    return JsonResponse({'all_Insta_Acc':list_data})


@csrf_exempt
def reg_user(req):
    user_name=req.POST.get("name","").strip()           #strip() removes unwanted spaces at the beginning and end of the input.
    user_email=req.POST.get("email","").strip()
    user_mob=req.POST.get("mobile","").strip()
    file_obj=req.FILES["imgg"]


    is_valid_file, msg=validate_file(file_obj)

    if is_valid_file:
        pass
    else:
        return HttpResponse(msg)
    

    new_user= User.objects.create(name=user_name, email=user_email, mobile=user_mob, imgg=file_obj)

    try:
        new_user.full_clean()               #full_clean() is a built-in Django method that runs all validations on the model fields before saving.
    except ValidationError as e:            #without this, model field validations (like regex) won't work. invalid data will be saved directly to DB.
        if e.message_dict:
            # Get first field name error
            field = list(e.message_dict.keys())[0]
            error_text = e.message_dict[field][0]
            return JsonResponse({'error': error_text}, status=400)
        return HttpResponseBadRequest({'errors':e.message_dict},status=400)
    return HttpResponse('Succesfully reg!')


@csrf_exempt
def delete_user(req, id):
    if req.method != "DELETE":
        return JsonResponse({"error": "Only DELETE method allowed"}, status=405)

    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    user.delete()
    return JsonResponse({"message": "User deleted successfully!"}, status=200)













































# from django.shortcuts import render
# from django.http import JsonResponse, HttpResponseBadRequest
# from django.views.decorators.csrf import csrf_exempt
# from .models import User
# from .forms import UserForm

# # File validation function
# def validate_file(file_obj):
#     max_size = 4 * 1024 * 1024  # 4MB
#     if file_obj.size > max_size:
#         return False, "File is too large. Max size is 4MB."
    
#     allowed_types = ["image/jpeg", "image/png"]
#     if file_obj.content_type not in allowed_types:
#         return False, "Invalid file type. Allowed: JPG, PNG only."

#     return True, "Valid File"


# # Get all users (JSON Response)
# def get_user(req):
#     all_users = User.objects.all().values()
#     return JsonResponse({'all_users': list(all_users)})


# @csrf_exempt
# def reg_user(req):
#     if req.method != "POST":
#         return JsonResponse({'error': 'Only POST method allowed'}, status=405)

#     # Use ModelForm to validate input fields
#     form = UserForm(req.POST, req.FILES)

#     # Check if form fields are valid
#     if not form.is_valid():
#         # Returns field-wise validation errors (name & mobile regex errors also show here)
#         return JsonResponse({'errors': form.errors}, status=400)

#     # Check file validation manually
#     file_obj = req.FILES.get("imgg")
#     if file_obj:
#         is_valid_file, msg = validate_file(file_obj)
#         if not is_valid_file:
#             return HttpResponseBadRequest(msg)

#     # If everything is valid -> Save User
#     form.save()
#     return JsonResponse({'message': 'Successfully registered!'}, status=201)
