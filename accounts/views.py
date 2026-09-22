from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserEditForm, ProfileEditForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import User

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request,
                username=data['username'],
                password=data['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home_page')
                else:
                    return HttpResponse('Profilingiz faol emas')
            else:
                return HttpResponse("Username yoki parol noto'g'ri")
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'account/login.html', context)

def user_logout(request):
    logout(request)
    return redirect('home_page')

@login_required
def user_profile(request):
    context = {
        'user': request.user
    }
    return render(request, 'account/user_profile.html', context)

def user_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home_page')
    else:
        form = RegisterForm()
        
    context = {
        'form':form
    }
    return render(request, 'account/register.html', context)
            

class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'account/profile_edit.html', context)

    def post(self, request):
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'account/profile_edit.html', context)


@login_required
@user_passes_test(lambda u:u.is_staff)
def admin_panel(request):
    admin_users = User.objects.filter(is_superuser =True)
    context = {
         'admin_users':admin_users
     }
    
    return render(request, 'pages/admin_panel.html', context)
    