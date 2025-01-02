from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from app01 import models
import datetime

class Tracer(object):
    def __init__(self):
        self.user = None
        self.price_policy = None


class AuthMiddleware(MiddlewareMixin):
    def process_request(self,request):
        request.tracer = Tracer()

        user_id = request.session.get('user_id',0)
        user_object = models.UserInfo.objects.filter(id=user_id).first()
        request.tracer.user = user_object

        ### 判断当前url是否可以访问
        if not request.tracer.user and request.path_info in settings.WHITE_REGEX_URL_LIST:
            return
        if not request.tracer.user:
            url = reverse('home')
            return redirect(url)

        settings.WHITE_REGEX_URL_LIST.remove('/')
        if request.tracer.user and request.path_info in settings.WHITE_REGEX_URL_LIST:
            settings.WHITE_REGEX_URL_LIST.append('/')
            return redirect('/project/list')

        settings.WHITE_REGEX_URL_LIST.append('/')

        ## 将用户信息和对应价格类型封装到 request
        _object = models.Transaction.objects.filter(user=user_object,status=2).order_by('-id').first()
        ## 如果时间为空或结束时间过期都改为免费版
        if _object.end_datetime is None or _object.end_datetime < datetime.datetime.now():
            _object = models.Transaction.objects.filter(user=user_object,status=2,price_policy=1).first()
        request.tracer.price_policy = _object.price_policy







