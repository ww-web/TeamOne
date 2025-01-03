from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.

#### 用户者表
class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名',max_length=32)
    email = models.EmailField(verbose_name='邮箱',max_length=32)
    mobile_phone = models.CharField(verbose_name='手机号',max_length=16)
    password = models.CharField(verbose_name='密码',max_length=32)

#### 产品价格表
class Price(models.Model):
    category_choices = (
        (1, '免费版'),
        (2, 'vip'),
        (3, 'svip'),
    )
    category = models.SmallIntegerField(verbose_name='产品', choices=category_choices, default=1)
    ## PositiveIntegerField 表示正整数类型
    price = models.PositiveIntegerField(verbose_name='价格/人/年')
    projects_num = models.PositiveIntegerField(verbose_name='项目总数')
    projects_member = models.PositiveIntegerField(verbose_name="项目成员数")
    project_space = models.PositiveIntegerField(verbose_name="每项目空间")
    create_datatime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

#### 交易表
class Transaction(models.Model):
    status_choice = (
        (1,'未支付'),
        (2,'已支付'),
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choice)
    user = models.ForeignKey(verbose_name='用户', to="UserInfo")
    price_policy = models.ForeignKey(verbose_name='价格', to="Price")

    count = models.IntegerField(verbose_name='数量(年)',help_text='0 表示无期限')
    price = models.IntegerField(verbose_name='实际金额')
    start_datetime = models.DateTimeField(verbose_name='开始时间', null=True, blank=True)
    end_datetime = models.DateTimeField(verbose_name='结束时间', null=True, blank=True)
    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    ### unique=True 表示 唯一索引
    order = models.CharField(verbose_name='订单号', max_length=64, unique=True)

#### 项目表
class Project(models.Model):
    COLOR_CHOICES = (
        (1, "#56b8eb"),  # 56b8eb
        (2, "#f28033"),  # f28033
        (3, "#ebc656"),  # ebc656
        (4, "#a2d148"),  # a2d148
        (5, "#20BFA4"),  # #20BFA4
        (6, "#7461c2"),  # 7461c2,
        (7, "#20bfa3"),  # 20bfa3,
    )
    name = models.CharField(verbose_name='项目名', max_length=32)
    color = models.SmallIntegerField(verbose_name='颜色', choices=COLOR_CHOICES, default=1)
    desc = models.CharField(verbose_name="项目描述", max_length=255,null=True,blank=True)
    use_space = models.IntegerField(verbose_name='项目已使用空间',default=0)
    star = models.BooleanField(verbose_name='星标',default=False)

    join_count = models.SmallIntegerField(verbose_name='参与人数', default=1)
    creator = models.ForeignKey(verbose_name='创建者', to=UserInfo)
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

#### 参与者表
class ProjectUser(models.Model):
    user = models.ForeignKey(verbose_name='参与者', to='UserInfo')
    project = models.ForeignKey(verbose_name='项目', to="Project")
    star = models.BooleanField(verbose_name='星标', default=False)
    create_datetime = models.DateTimeField(verbose_name='加入时间', auto_now_add=True)