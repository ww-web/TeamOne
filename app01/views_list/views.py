from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
# Create your views_list here.
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.http import JsonResponse
from django.db.models import Q
import uuid
import datetime

from app01 import models
from app01.forms import account
from utils.image_code import check_code

# @csrf_exempt
def register(request):
    if request.method == 'GET':
        form = account.myforms()
        return render(request,'register.html',{'form': form})

    form = account.myforms(data=request.POST)
    if form.is_valid():
        instance = form.save()
        policy_object = models.Price.objects.filter(category=1).first()
        models.Transaction.objects.create(
            status=1,
            user=instance,
            price_policy=policy_object,
            count=0,
            price=0,
            start_datetime=datetime.datetime.now(),
            order=str(uuid.uuid4)
        )
        return JsonResponse({'status': True,'data':'/login'})
    # return render(request,'register.html',{'form': form})
    return JsonResponse({'status': False,'error': form.errors})

def send_sms(request):
    form = account.SendSmsForm(request,data=request.GET)
    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({'status': False,'error': form.errors})

#################################### 短信登录
def login(request):
    if request.method == 'GET':

        initial_data = {}
        ## 我们想要填充的字段名为'mobile_phone'，并且期望的GET参数是'phone'
        # 获取URL中的GET参数,如果'phone'不存在,# 默认为空字符串，
        my_field_value = request.GET.get('phone', '')
        # 将获取的值添加到初始数据字典中
        initial_data['mobile_phone'] = my_field_value
        # 创建表单实例，并传入initial_data作为初始值
        form = account.login(initial=initial_data)

        return render(request,'login.html',{'form':form})
    form = account.login(data=request.POST)
    if form.is_valid():
        # form.save()
        models_phone = form.cleaned_data['mobile_phone']
        user_object = models.UserInfo.objects.filter(models_phone=models_phone).first()
        request.session['user_id'] = user_object.id
        url = reverse('home')
        return JsonResponse({'status': True,'data': '/project/list' })
    return JsonResponse({'status': False,'error': form.errors})

#################################### 密码登录
def login_password(request):
    if request.method == 'GET':
        form = account.login_password(request)
        return render(request,'login_password.html',{'form':form})
    form = account.login_password(request,data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user_object = models.UserInfo.objects.filter(Q(email=username)|Q(mobile_phone=username)).filter(password=password).first()
        if user_object:
            request.session['user_id'] = user_object.id
            request.session.set_expiry(60 * 60 * 24 * 14)
            url = reverse('home')
            return redirect('/project/list')
        form.add_error('username','账号或密码错误，请重试')
    return render(request,'login_password.html',{'form':form})

#################################### 密码登录-图像验证码
def image_code(request):
    img_object,code = check_code()

    request.session['image_code'] = code
    request.session.set_expiry(60)

    stream = BytesIO()
    img_object.save(stream,'png')

    return HttpResponse(stream.getvalue())

#################################### 首页
def home(request):
    return render(request,'home.html')

#################################### 退出当前账号
def logout(request):
    request.session.flush()

    url = reverse('home')
    return HttpResponseRedirect(url)
