from django.shortcuts import render
from .models import Laptop
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
#Getting Data
def get_info(req):
    lap_data=Laptop.objects.all()
    dict_data=lap_data.values()
    list_data=list(dict_data)
    return JsonResponse({'all_data':list_data})


#Posting Data
@csrf_exempt 
def reg_info(req):
    emp_data=json.loads(req.body)
    id=emp_data['lap_id']
    brand=emp_data['lap_brand']
    specs=emp_data['lap_specs']
    price=emp_data['lap_price']
    new_info=Laptop.objects.create(lap_id=id,lap_brand=brand,lap_specs=specs,lap_price=price)
    return JsonResponse({'msg':'Succesfully Created'})


#Updating(Post & Patch) Data
@csrf_exempt
def update_info(req,id):
    try:
        lap_data=json.loads(req.body)
    except json.JSONDecodeError:
        return JsonResponse({'Error':'Invalid Json'})

    try:
        lap=Laptop.objects.get(lap_id=id)
    except Laptop.DoesNotExist:
        return JsonResponse({'Error':'Info Not Found'})
    
    if 'lap_id' in lap_data:
        lap.lap_id=lap_data['lap_id']
    if 'lap_brand' in lap_data:
        lap.lap_brand=lap_data['lap_brand']
    if 'lap_specs' in lap_data:
        lap.lap_specs=lap_data['lap_specs']
    if 'lap_price' in lap_data:
        lap.lap_price=lap_data['lap_price']
    lap.save()      #saving updated data
    return JsonResponse({'success':'Info Updated'})


#Deleting Data
@csrf_exempt
def delete_info(req,id):
    try:
        existing_info=Laptop.objects.get(lap_id=id)
        existing_info.delete()
        return JsonResponse({'Succes':'Info Deleted'})
    except:
        return HttpResponse('Info Not Found')
