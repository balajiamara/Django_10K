from django.shortcuts import render
from .models import Insta_Acc
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.http.multipartparser import MultiPartParser
from .serializers import InstaAccSerializer
import json
import cloudinary
from django.forms.models import model_to_dict



def validate_file(file_obj):
    max_size=5*1024*1024
    if file_obj.size>max_size:
        return False, 'File size exceeds the maximum limit of 5MB.'
    
    allowed_types=['image/jpeg','image/png',]
    if file_obj.content_type not in allowed_types:
        return False, 'Unsupported file type. Only JPEG and PNG are allowed.'
    return True, 'File is valid.'

# Create your views here.
def get_Insta_Acc(request):
    insta_data=Insta_Acc.objects.all()
    dict_dat=insta_data.values()
    list_data=list(dict_dat)
    return JsonResponse({'all_Insta_Acc':list_data})

@csrf_exempt
def reg_Insta_Acc(request):
    try:
        id=request.POST.get('userid')
        username=request.POST.get('username')
        pw=request.POST.get('password')
        em=request.POST.get('email')
        pp=request.FILES['profile_pic']         #or use request.FILES.get('profile_pic')
        img_url=cloudinary.uploader.upload(pp)   
        print(img_url["secure_url"])



        is_valid, msg=validate_file(pp)
        if not is_valid:
            return JsonResponse({'Error':msg})
        # else:
        #     return HttpResponse(msg)

        new_acc=Insta_Acc.objects.create(userid=id,username=username,password=pw,email=em,profile_pic=img_url["secure_url"])
        # return JsonResponse({'Message': 'Insta Account Registered Successfully',"details":list(new_acc.values)})
        return JsonResponse({
        'Message': 'Insta Account Registered Successfully',
        'details': model_to_dict(new_acc)
        })
    except Exception as e:
        return JsonResponse({'Error':str(e)}, status=400)
    return JsonResponse({'Error':'Invalid Request Method'}, status=405)

@csrf_exempt
def update_Insta_Acc(request,id):
    # try:
    #     insta_data=json.loads(request.body)
    # except json.JSONDecodeError:
    #     return JsonResponse({'Error':'Invalid Json Data'})
    
    try:
        insta=Insta_Acc.objects.get(userid=id)
    except Insta_Acc.DoesNotExist:
        return JsonResponse({'Error':'Insta Account Not Found'})
    
    if request.method in ['PUT', 'PATCH']:
         # Manually parse multipart form data
        content_type = request.META.get('CONTENT_TYPE', '')
        if 'multipart/form-data' in content_type:
            upload_handlers = [TemporaryFileUploadHandler(request)]
            parser = MultiPartParser(request.META, request, upload_handlers=upload_handlers)
            data, files = parser.parse()
        else:
            return JsonResponse({'Error': 'Expected multipart form data'}, status=400)

        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        profile_pic = files.get('profile_pic')

        if username:
            insta.username = username
        if password:
            insta.password = password
        if email:
            insta.email = email
        if profile_pic:
            insta.profile_pic = profile_pic

        insta.save()
        return JsonResponse({'Message': 'Insta Account Updated Successfully'})

    return JsonResponse({'Error': 'Only PUT/PATCH allowed'}, status=405)
    


@csrf_exempt
def delete_Insta_Acc(request,id):
    try:
        insta=Insta_Acc.objects.get(userid=id)
    except Insta_Acc.DoesNotExist:
        return JsonResponse({'Error':'Insta Account Not Found'})
    insta.delete()
    return HttpResponse("Insta Account Deleted Successfully")




# from django.shortcuts import render
# from django.http import JsonResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from .models import Insta_Acc
# from .serializers import InstaAccSerializer
# import json


# def get_Insta_Acc(request):
#     """Fetch all Insta accounts"""
#     insta_data = Insta_Acc.objects.all()
#     serializer = InstaAccSerializer(insta_data, many=True)
#     return JsonResponse({'all_Insta_Acc': serializer.data}, safe=False)



# @csrf_exempt
# def reg_Insta_Acc(request):
#     if request.method == 'POST':
#         if not request.FILES:
#             return JsonResponse({'error': 'No file uploaded. Use multipart/form-data.'}, status=400)

#         # Merge POST + FILES together for the serializer
#         data = request.POST.dict()
#         data['profile_pic'] = request.FILES.get('profile_pic')

#         serializer = InstaAccSerializer(data=data)

#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse({
#                 'message': 'Insta Account Registered Successfully',
#                 'data': serializer.data
#             }, status=201)

#         return JsonResponse({'errors': serializer.errors}, status=400)

#     return JsonResponse({'error': 'Only POST method allowed'}, status=405)



# @csrf_exempt
# def update_Insta_Acc(request, id):
#     if request.method not in ['PUT', 'PATCH']:
#         return JsonResponse({'error': 'Only PUT/PATCH allowed'}, status=405)

#     try:
#         insta = Insta_Acc.objects.get(userid=id)
#     except Insta_Acc.DoesNotExist:
#         return JsonResponse({'error': 'Account not found'}, status=404)

#     # ✅ copy() because request.POST is immutable
#     data = request.POST.copy()
#     files = request.FILES

#     # ✅ Merge files manually into data
#     for key, value in files.items():
#         data[key] = value

#     serializer = InstaAccSerializer(insta, data=data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return JsonResponse({
#             'message': 'Account updated successfully',
#             'data': serializer.data
#         }, status=200)
#     else:
#         return JsonResponse({'errors': serializer.errors}, status=400)



# @csrf_exempt
# def delete_Insta_Acc(request, id):
#     """Delete Insta account"""
#     try:
#         insta = Insta_Acc.objects.get(userid=id)
#         insta.delete()
#         return JsonResponse({'message': 'Account deleted successfully'})
#     except Insta_Acc.DoesNotExist:
#         return JsonResponse({'error': 'Account not found'}, status=404)
