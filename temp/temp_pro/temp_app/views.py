from django.shortcuts import render
from .models import Company
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.http.multipartparser import MultiPartParser
from datetime import datetime 

# Create your views here.
def get_info(req):
    all_details=Company.objects.all()
    dict_data=all_details.values()
    list_data=list(dict_data)
    return JsonResponse({'Details':list_data})


@csrf_exempt
def reg_info(req):
    if req.method!='POST':
        return HttpResponse('POST method only allowed')
    
    namee=req.POST.get('name')
    emaill=req.POST.get('email')
    capitall=req.POST.get('capital')
    typee=req.POST.get('type')
    start_datee=req.POST.get('start_date')

    errors={}

    if not namee:
        errors['name']='This field is required'
    if not emaill:
        errors['email']='This field is required'
    if not capitall:
        errors['capital']='This field is required'
    if not start_datee:
        errors['start_date']='This field is required'

    if capitall:
        try:
            capitall=int(capitall)
        except ValueError:
            return HttpResponse('capital must be in Integer')

    if start_datee:
        try:
            start_datee=datetime.strptime(start_datee,'%Y-%m-%d').date()
        except ValueError:
            return HttpResponse('Invalid date Date must be in YYYY-MM-DD format')
    else:
        start_date=None

    if typee not in [Company.Type.MNC, Company.Type.Startup]:
        errors['type']="Type must be 'M'(MNC) or 'S'(StartUp) "

    if errors:
        return JsonResponse({'errors':errors}, status=400)

    company=Company.objects.create(
        name=namee,
        email=emaill,
        capital=capitall,
        type=typee,
        start_date=start_datee
    )

    return JsonResponse({
        'msg':'Company created successfully',
        'company':{
            'id':company.id,
            'name':company.name,
            'email':company.email,
            'capital':company.capital
        }
    },status=201)

# @csrf_exempt
# def update_info(req,id):
#     if req.method not in ['PUT','PATCH']:
#         return HttpResponse('Only PUT or PATCH allowed', status=400)

#     try:
#         companyy=Company.objects.get(id=id)
#     except Company.DoesNotExist:
#         return HttpResponse('Company Not Found', status=404)

#     from urllib.parse import parse_qs

#     raw_data=req.body.decode('utf-8')
#     form = parse_qs(raw_data)

#     def get_value(key):
#         return form.get(key,[None])[0]
    
#     namee=get_value('name')
#     emaill=get_value('email')
#     capitall=get_value('capital')
#     typee=get_value('type')
#     start_datee=get_value('start_date')

#     error={}

#     if namee:
#         companyy.name=namee
#     if emaill:
#         companyy.email=emaill
#     if capitall:
#         try:
#          companyy.capital=int(capitall)
#         except:
#             return JsonResponse({'error':'capital must be an integer'},status=400)
    
#     if start_datee:
#         try:
#             companyy.start_date=datetime.strptime(start_datee, '%Y-%m-%d').date()
#         except:
#             return JsonResponse({'error':'start_date must be in YYYY-MM-DD format'},status=400)
        
#     if typee:
#         if typee not in [Company.Type.MNC, Company.Type.Startup]:
#             return JsonResponse({'error':'Type must be M or S'}, status=400)
#         companyy.type=typee

#     companyy.save()

#     return JsonResponse({
#         'msg': 'Company updated successfully',
#         'company': {
#             'id': companyy.id,
#             'name': companyy.name,
#             'email': companyy.email,
#             'capital': companyy.capital,
#             'type': companyy.type,
#             'start_date': companyy.start_date.isoformat(),
#         }
#     }, status=200)

@csrf_exempt
def update_info(req, id):
    try:
        company = Company.objects.get(id=id)
    except Company.DoesNotExist:
        return JsonResponse({'Error': 'Company Not Found'}, status=404)

    if req.method not in ['PUT', 'PATCH']:
        return JsonResponse({'Error': 'Only PUT/PATCH methods are allowed'}, status=405)

    # Detect multipart form-data
    content_type = req.META.get('CONTENT_TYPE', '')
    if 'multipart/form-data' in content_type:
        upload_handlers = [TemporaryFileUploadHandler(req)]
        parser = MultiPartParser(req.META, req, upload_handlers=upload_handlers)
        data, files = parser.parse()
    else:
        return JsonResponse({'Error': 'Expected multipart/form-data'}, status=400)

    # Extract fields
    name = data.get('name')
    email = data.get('email')
    capital = data.get('capital')
    typee = data.get('type')
    start_date = data.get('start_date')

    # Update fields ONLY if present
    if name:
        company.name = name
    
    if email:
        company.email = email

    if capital:
        try:
            company.capital = int(capital)
        except:
            return JsonResponse({'error': 'capital must be an integer'}, status=400)

    if start_date:
        try:
            company.start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        except:
            return JsonResponse({'error': 'start_date must be YYYY-MM-DD'}, status=400)

    if typee:
        if typee not in [Company.Type.MNC, Company.Type.Startup]:
            return JsonResponse({'error': 'type must be M or S'}, status=400)
        company.type = typee

    company.save()

    return JsonResponse({'Message': 'Company updated successfully'})


@csrf_exempt
def del_info(req, id):
    # Allow only DELETE
    if req.method != 'DELETE':
        return JsonResponse({'Error': 'Only DELETE method is allowed'}, status=405)

    # Try fetching the company
    try:
        company = Company.objects.get(id=id)
    except Company.DoesNotExist:
        return JsonResponse({'Error': 'Company Not Found'}, status=404)

    # Delete the company
    company.delete()

    return JsonResponse({'Message': 'Company deleted successfully'}, status=200)