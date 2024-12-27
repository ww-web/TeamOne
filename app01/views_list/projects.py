from django.shortcuts import render
from django.http import JsonResponse
from app01.forms import projectForm
from app01 import models



def project_list(request):
    if request.method == 'GET':
        form_a = projectForm.projectCreateForm(request)
        form_b = projectForm.projectListForm()
        projects = models.Project.objects.all()
        return render(request,'poject_list.html',{'form_a':form_a,'form_b':form_b,'projects':projects})

    form = projectForm.projectListForm(request,data=request.POST)
    if form.is_valid():
        form.instance.creator = request.tracer.user
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status':False,'error':form.errors})