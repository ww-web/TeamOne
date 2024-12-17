class BootStrapForm(object):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs = {'class':"form-control",'placeholder':f"请输入{field.label}"}