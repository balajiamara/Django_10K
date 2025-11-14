from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Check
import json
import bcrypt
import jwt
from datetime import datetime, timedelta
from django.conf import settings
SECRETKEY= settings.SECRET_KEY


# Create your views here.
@csrf_exempt 
def reg_user(req):
    user_data=json.loads(req.body)
    id=user_data['userid']
    name=user_data['username']
    pw=user_data['password']

    encrypted_password=bcrypt.hashpw(
        pw.encode("utf-8"),
        bcrypt.gensalt(14)
    ).decode("utf-8")
    print(encrypted_password)

    new_info=Check.objects.create(userid=id,username=name,password=encrypted_password)
    return JsonResponse({'msg':'Succesfully Created','data': {
                'userid': new_info.userid,
                'username': new_info.username
            }})

    



def get_user(req):
    user_data=Check.objects.all()
    dict_data=user_data.values()
    list_data=list(dict_data)
    return JsonResponse({'all_data':list_data})

@csrf_exempt
def login_user(req):
    try:
        user_data=json.loads(req.body)
        id=user_data['userid']
        pw=user_data['password']

        try:
            user=Check.objects.get(userid=id)
        except Check.DoesNotExist:
            return HttpResponse('User Not Found',status=404)

        if not bcrypt.checkpw(pw.encode('utf-8'),user.password.encode('utf-8')):
            return JsonResponse({'msg':'Wrong userid or password'},status=401)
        #     return JsonResponse({
        #         'msg':'login success',
        #         'data':{
        #             'userid':user.userid,
        #             'username':user.username
        #         }
        #     })
        # else:
        #     return HttpResponse('Wrong userid or password', status=401)
        

        now=datetime.utcnow()
        exp=now+timedelta(seconds=30)
        payload={
            'userid':user.userid,
            'username':user.username,
            'iat':now,
            'exp':exp
        }

        token=jwt.encode(payload,SECRETKEY,algorithm='HS256')
        print(token)

        # return JsonResponse({
        #     'msg': 'login success',
        #     'access_token': token,
        #     'expires_at': exp.isoformat() + 'Z',     #Converts expiry datetime into a clean, standard format with 'Z' UTC timezone
        #     'data': {
        #         'userid': user.userid,
        #         'username': user.username
        #     }
        # })
    
        res=HttpResponse('cookie is set in the browser')
        res.set_cookie(
            key='my_cookie',
            value=token,
            httponly=True,
            max_age=20
        )

        return res
        

    except Exception as e:
        return JsonResponse({'error':str(e)},status=400)
    