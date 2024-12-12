from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import random
from django.conf import settings

from app01 import models
from utils.tencent.sms import send_sms_single
from django_redis import get_redis_connection
from utils import encrypt


### 注册页面
class myforms(forms.ModelForm):
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^1\d{10}$', '请输入正确的手机号')])
    password = forms.CharField(label='密码', min_length=8,max_length=18,error_messages={
        'min_length': '密码长度太短',
        'max_length': '密码长度太长'
    },widget=forms.PasswordInput())

    confirm_password = forms.CharField(label='重复密码', min_length=8,max_length=18,error_messages={
        'min_length': '密码长度太短',
        'max_length': '密码长度太长'
    }, widget=forms.PasswordInput())
    code = forms.CharField(label='验证码')

    class Meta:
        model = models.UserInfo
        fields = '__all__'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,filed in self.fields.items():
            filed.widget.attrs = {'class':"form-control",'placeholder': f"请输入{filed.label}"}

    # 校验手机号
    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exist = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exist:
            raise ValidationError('手机号已存在')
        return mobile_phone
    # 校验密码
    def clean_password(self):
        passwd = self.cleaned_data['password']
        return encrypt.md5(passwd)
        # return passwd
    # 校验重复密码
    def clean_confirm_password(self):
        passwd = self.cleaned_data['password']
        confirm_passwd = encrypt.md5(self.cleaned_data['confirm_password'])
        # confirm_passwd = self.cleaned_data('confirm_password')
        if passwd != confirm_passwd:
            raise ValidationError("密码不一致，请重试")
        return confirm_passwd
    # 验证码校验
    def clean_code(self):
        mobile = self.cleaned_data.get('mobile_phone')
        code = self.cleaned_data['code']
        if not mobile:
            return code

        conn = get_redis_connection()
        redis_code = conn.get(mobile)
        if not redis_code:
            raise ValidationError('验证码失效或未发送，请重新发送 ')

        redis_str_code = redis_code.decode('utf-8')
        if redis_str_code != code:
            raise ValidationError('验证码错误')
        return code


########## 点击获取验证码 Form
class SendSmsForm(forms.Form):
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^1\d{10}$', '请输入正确的手机号')])

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request = request

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        tpl = self.request.GET.get('tpl')

        template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
        if not template_id:
            raise ValidationError("短信模板错误")

        if tpl == 'register':
            exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
            if exists:
                raise ValidationError('手机号已存在')
        elif tpl == 'login':
            exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
            if not exists:
                raise ValidationError('该手机号码未注册，请注册后再试')

        code = random.randrange(1000,9999)
        sms = send_sms_single(mobile_phone,template_id,[code, ])
        if sms['result'] != 0:
            raise ValidationError("短信发送失败，{}".format(sms['errmsg']))

        print('发送没')
        conn = get_redis_connection()
        conn.set(mobile_phone,code,ex=60)

        return mobile_phone

################## 登录页面
class login(forms.ModelForm):
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^1\d{10}$', '请输入正确的手机号')])
    code = forms.CharField(label="验证码")

    class Meta:
        model = models.UserInfo
        fields = ['mobile_phone','code']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs = {'class':"form-control",'placeholder':f"请输入{field.label}"}

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if not exists:
            raise ValidationError('该手机号码未注册，请注册后再试')
        return mobile_phone

    def clean_code(self):
        mobile_phone = self.cleaned_data.get('mobile_phone')
        code = self.cleaned_data['code']
        if not mobile_phone:
            return code

        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)
        if not redis_code:
            raise ValidationError('验证码发送失败或未发送，请重试')
        redis_str_code = redis_code.decode('utf-8')
        if code != redis_str_code:
            raise ValidationError('验证码错误')
        return code

############## 密码登录页面
class login_password(forms.ModelForm):
    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^1\d{10}$', '请输入正确的手机号')])
    password = forms.CharField(label='密码', min_length=8, max_length=18, error_messages={
        'min_length': '密码长度太短',
        'max_length': '密码长度太长'
    }, widget=forms.PasswordInput())

    class Meta:
        model = models.UserInfo
        fields = ['mobile_phone','password']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs = {'class':"form-control",'placeholder':f"请输入{field.label}"}

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if not exists:
            raise ValidationError('手机号未注册，请先注册后再试')
        return mobile_phone

    def clean_password(self):
        passwd = encrypt.md5(self.cleaned_data['password'])
        mobile_phone = self.cleaned_data.get('mobile_phone')
        if not mobile_phone:
            return passwd
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone,password=passwd).first()
        if not exists:
            raise ValidationError('请输入正确密码')
        return passwd










