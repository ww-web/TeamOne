from django import forms
from django.core.validators import ValidationError
from app01 import models
from app01.forms.bootstrap import BootStrapForm



class projectCreateForm(BootStrapForm,forms.ModelForm):

    class Meta:
        model = models.Project
        fields = ['name','color','desc']
        widgets = {
            'desc': forms.Textarea
        }

    def __init__(self,request,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.request = request

    def clean_name(self):
        name = self.cleaned_data['name']
        creator = self.request.tracer.user

        exists = models.Project.objects.filter(creator=creator,name=name).exists()
        if exists:
            raise ValidationError('项目名已存在')

        num = self.request.tracer.price_policy.projects_num
        count = models.Project.objects.filter(creator=creator).count()
        if count >= num:
            raise ValidationError("项目已超额，请升级")
        return name

