from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.http.multipartparser import MultiPartParser
from .serializers import MenuSerializer
from .models import Menu
import json


# def validate_file(file):
#     max

# Create your views here.
def get_dish(req):
    all_menu=Menu.objects.all()
    dict_data=all_menu.values()
    list_data=list(dict_data)
    return JsonResponse({'Menu_card':list_data})

# @csrf_exempt
# def add_dish(req):
#     id=req.POST.get('DishId')
#     name=req.POST['DishName']
#     ingre=req.POST['Ingredients']
#     price=req.POST.get('Price')
#     pic=req.FILES.get('Image')


#     new_item=Menu.objects.create(DishId=id,DishName=name,Ingredients=ingre,Price=price,Image=pic)
#     return JsonResponse({'msg':'Dish Added Successfully'})



@csrf_exempt
def add_dish(req):
    if req.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

    # Combine POST and FILES manually
    data = req.POST.copy()
    if req.FILES:
        data.update(req.FILES)

    serializer = MenuSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'msg': 'Dish Added Successfully'}, status=201)
    else:
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def update_dish(req,id):
    try:
        menu=Menu.objects.get(DishId=id)
    except Menu.DoesNotExist:
        return JsonResponse({'Error':'Dish Not Found'})
    
    if req.method in ['PUT', 'PATCH']:
        content_type=req.META.get('CONTENT_TYPE','')
        if 'multipart/form-data' in content_type:
            upload_handlers=[TemporaryFileUploadHandler(req)]
            parser=MultiPartParser(req.META, req, upload_handlers=upload_handlers)
            data,files=parser.parse()
        else:
            return JsonResponse({'Expected multipart form data'}, status=400)
        

        name = data.get('DishName')
        ingre = data.get('Ingredients')
        price = data.get('Price')
        pic = files.get('Image')


        if name:
            menu.DishName=name
        if ingre:
            menu.Ingredients=ingre
        if price:
            menu.Price=price
        if pic:
            menu.Image=pic

        menu.save()
        return JsonResponse({'Message':'Menu is succesfully Updated'})
    return JsonResponse({'Error':'Only PUT/PATCH methods are allowed'}, status=405)
        

@csrf_exempt
def del_dish(req,id):
    try:
        menu=Menu.objects.get(DishId=id)
    except Menu.DoesNotExist:
        return JsonResponse({'Error':'ID Not found'})
    menu.delete()
    return HttpResponse('Item is Succesfully Deleted')