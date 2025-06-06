from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm
# Create your views here.

def register_view(request):
    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user =form.save()
            login(request, user)
            messages.success(request,"Account created sccessfully.")
            return redirect('core:user_dashboard')
    else:
        form = CustomUserCreationForm()
        return render(request,"users/register.html",{'form':form })

@login_required
def profile_view(request):
    return render (request,"users/profile.html",{'user':request.user})

@login_required
def edit_profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileEditForm(instance = user)
    return render(request,'users/edit_profile.html',{'form':form})
