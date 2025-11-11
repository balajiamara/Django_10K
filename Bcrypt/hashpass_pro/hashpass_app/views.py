from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Check
import json

# Create your views here.
@csrf_exempt 
def reg_user(req):
    user_data=json.loads(req.body)
    id=user_data['userid']
    name=user_data['username']
    pw=user_data['password']
    new_info=Check.objects.create(userid=id,username=name,password=pw)
    return JsonResponse({'msg':'Succesfully Created'})      #,json.dumps(new_info)


def get_user(req):
    user_data=Check.objects.all()
    dict_data=user_data.values()
    list_data=list(dict_data)
    return JsonResponse({'all_data':list_data})


def login_user():
    pass