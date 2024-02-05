from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Records

def home(req):
    records = Records.objects.all()

    # Check if user is logging in
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        # authenticate user
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            messages.success(req, "Log in Successful!")
            return redirect('home')
        else:
            messages.success(req, "There was an error logging in.")
            return redirect('home')

    else:
        return render(req, 'home.html', {'records':records})

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
    
def delete_record(req, key):
    if req.user.is_authenticated:
        to_be_deleted = Records.objects.get(id=key)
        to_be_deleted.delete()
        messages.success(req, "Record successfully deleted.")
        return redirect('home')
    else:
        messages.success(req, "You must be logged in to do that.")
        return redirect('home')
    
def add_record(req):
    form = AddRecordForm(req.POST or None)
    if req.user.is_authenticated:
        if req.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(req, "Record added.")
                return redirect('home')
        return render(req, 'add_record.html', {'form':form})
    else:
        messages.success(req, "You must be logged in to do that.")
        return redirect('home')

def customer_record(req, key):
    if req.user.is_authenticated:
        # get record with key
        current_record = Records.objects.get(id=key)
        form = AddRecordForm(req.POST or None, instance=current_record)
        return render(req, 'record.html', {'customer_record':current_record, 'form':form})
    else:
        messages.success(req, "You must be logged in to do that.")
        return redirect('home')
    
def update_record(req, key):
    if req.user.is_authenticated:
        current_record = Records.objects.get(id=key)
        form = AddRecordForm(req.POST or None, instance=current_record)
        if req.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(req, "Record has been updated.")
                return redirect('home')
    else:
        messages.success(req, "You must be logged in to do that.")
        return redirect('home')
