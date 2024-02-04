from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm

def home(req):
    # Check if user is logging in
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        # authenticate user
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            messages.success(req, "You have been logged in.")
            return redirect('home')
        else:
            messages.success(req, "There was an error logging in.")
            return redirect('home')

    else:
        return render(req, 'home.html', {})

def login_user(req):
    pass

def logout_user(req):
    logout(req)
    messages.success(req, "Logout Successful!")
    return redirect('home')

def register_user(req):
    if req.method == 'POST':
        form = SignUpForm(req.POST)
        if form.is_valid():
            form.save()
            # Log user in after registration
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(req, user)
            messages.success(req, "Registration Successful! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(req, 'register.html', {'form':form})
    
    return render(req, 'register.html', {'form':form})
