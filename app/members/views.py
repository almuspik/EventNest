from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from members.forms import RegisterUserForm
# Create your views here.

def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save() 
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration Successfull!!!!"))
            return redirect('home')

    else:        
        form = RegisterUserForm()
         
    return render(request, 'register_user.html', {'form':form,})


def logout_user(request):
    logout(request)
    messages.success(request, ("Logout Pnaiiyaachu da Mapla "))
    return redirect('home')

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ("Olunga Login Pannu da Mapla...... "))
            return redirect('login')

    else:
        return render(request, 'login.html',{})
    

