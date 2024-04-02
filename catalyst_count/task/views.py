from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
import pandas as pd
import os
from task.utils import save_file
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from task.serializers import CompanySerializer
from django.db.models import (
    Q,
)
from task.models import Company
from .models import ChunkedUpload
from django.http import JsonResponse
from datetime import datetime

from django.contrib.auth import get_user_model
User = get_user_model()



class UserList(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = User.objects.all()
        context = {"users":user}
        return render(request,'task/user_list.html',context)
    

class UploadFile(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request,'task/upload.html')
    
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        file = request.FILES['the_file']
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        
        filepath = request.user.username + "_" + file.name
        
        print("PRINT_FILE_NAME",os.path.join(settings.MEDIA_ROOT, 'uploads',filepath))
        with open(os.path.join(upload_dir, filepath), 'ab') as destination:
        # with open(os.path.join(upload_dir, file.name), 'ab') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return JsonResponse({'progress': "done","file_path":filepath})

import json

def upload_complated(request):
    if request.method == 'POST':
        # Get the JSON data from the request body
        data = json.loads(request.body.decode('utf-8'))
        filepath = data.get("filepath")

        fullpath =  os.path.join(settings.MEDIA_ROOT, 'uploads',filepath)
        print(fullpath,"**********8")
        file_exists = os.path.exists(fullpath)
        if file_exists:
            ChunkedUpload.objects.create(
                filename = filepath,
                file_path = fullpath,
                user=request.user
            )

        save_file.delay(fullpath)
        
        return JsonResponse({"Response": "data"})
    

def query_builder(request):
    return render(request,'task/query_builder.html')



class Searh(APIView):
    serializer_class = CompanySerializer

    def get(self,request):
        name = request.GET.get('name',None)
        industory = request.GET.get('industry',None)
        year_founded = request.GET.get('year_founded',None)
        locality = request.GET.get('locality',None)
        country = request.GET.get('country',None)

        filter_dict  = {}
        if name is not None:
            filter_dict['name__icontains'] = name

        if industory is not None:
            filter_dict['industory'] = industory
        
        if year_founded is not None:
            filter_dict['year_founded'] = year_founded

        if country is not None:
            filter_dict['country'] = country

        
        print(filter_dict,"this filter dict")
        filter_dict = {k: v for k, v in filter_dict.items() if v}
        print(filter_dict,"after")

        
        filter_q = Q(**filter_dict)

        company = Company.objects.filter(filter_q)

        print(company.count(),"This is count")
        return Response({"message":self.serializer_class(company,many=True).data})

from django.shortcuts import get_object_or_404

def addUser(request,):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, email=email, password=password)
        return redirect('user_list')
    else:
        return render(request, 'task/user_add.html', {'message': "Add User"})

    
def editUser(request,id):
    
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = get_object_or_404(User,pk=id)

        user.username=username
        user.email=email
        user.password=password
        user.save()
        return redirect('user_list')
    user = get_object_or_404(User,pk=id)
    return render(request, 'task/user_edit.html', {'user': user})