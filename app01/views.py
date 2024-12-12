from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from app01.forms import account

# @csrf_exempt
def register(request):
    if request.method == 'GET':
        form = account.myforms()
        return render(request,'register.html',{'form': form})

    form = account.myforms(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True,'data':'/login'})
    # return render(request,'register.html',{'form': form})
    return JsonResponse({'status': False,'error': form.errors})

def send_sms(request):
    form = account.SendSmsForm(request,data=request.GET)
    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({'status': False,'error': form.errors})

def login(request):
    if request.method == 'GET':
        form = account.login()
        # return HttpResponse('登录')
        return render(request,'login.html',{'form':form})
    form = account.login(data=request.POST)
    if form.is_valid():
        # form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False,'error': form.errors})

def login_password(request):
    if request.method == 'GET':
        form = account.login_password()
        return render(request,'login_password.html',{'form':form})
    form = account.login_password(data=request.POST)
    if form.is_valid():
        return HttpResponse('登录成功')
    return render(request,'login_password.html',{'form':form})








