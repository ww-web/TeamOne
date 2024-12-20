"""webweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$',views.home,name='home'),
    url(r'^register/$', views.register,name="register"),
    url(r'^send/sms/$',views.send_sms,name="send_sms"),
    url(r'^login/$',views.login,name='login'),
    # 当短信登录，URL有一个参数时使用
    url(r'^login/(?P<param>\w+)/$',views.login,name='login'),
    url(r'login/password/',views.login_password,name='login_passwd'),
    url(r'^image/code/',views.image_code,name='img_code'),
    url(r'logout/$',views.logout,name='logout'),
]
