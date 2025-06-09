from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def admin_required(view_func):
    @login_required
    def wrapper(request,*args,**kwargs):
        if hasattr(request.user, 'role') and request.user.role =='ADMIN':
            return view_func(request,*args,**kwargs)
        return HttpResponseForbidden("Access denied.")
    return wrapper