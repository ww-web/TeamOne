from django.shortcuts import render
from django.http import JsonResponse
from app01.forms import projectForm



def project_list(request):
    if request.method == 'GET':
        form = projectForm.projectListForm(request)
        return render(request,'poject_list.html',{'form':form})

    form = projectForm.projectListForm(request,data=request.POST)
    if form.is_valid():
        form.instance.creator = request.tracer.user
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status':False,'error':form.errors})