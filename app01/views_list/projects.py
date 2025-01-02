from django.shortcuts import render
from django.http import JsonResponse
from app01.forms import projectForm
from app01 import models



def project_list(request):


    if request.method == 'GET':
        project_dict = {'star': [],'my': [],'join': []}

        form = projectForm.projectCreateForm(request)

        my_projects = models.Project.objects.filter(creator=request.tracer.user)
        for row in my_projects:
            if row.star:
                project_dict['star'].append({'value': row,'type': 'my'})
            else:
                project_dict['my'].append(row)
        join_project_list = models.ProjectUser.objects.filter(user=request.tracer.user)
        for item in join_project_list:
            if item.star:
                project_dict['star'].append({'value': item.project,'type':'join'})
            else:
                project_dict['join'].append(item.project)
        for i in project_dict['my']:
            print(i.name)
        return render(request,'poject_list.html',{'form':form,'project_dict':project_dict})

    form = projectForm.projectCreateForm(request,data=request.POST)
    if form.is_valid():
        form.instance.creator = request.tracer.user
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status':False,'error':form.errors})