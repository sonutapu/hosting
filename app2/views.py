import os
import django
django.setup()
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.contrib import messages
import time
import multiprocessing
import pyscreenshot
from datetime import datetime


# Create your views here.


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Email is exist ')
                return redirect(register)
            else:
                user = User.objects.create_user(username=username,
                                                password=password, email=email, first_name=first_name,
                                                last_name=last_name)
                user.set_password(password)
                user.save()
                print("success")
                return redirect('login_user')
        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect(register)
    else:
        # print("no post method")
        return render(request, 'register.html')
def take_screenshots():
    while True:
        datetimeNow = datetime.now()
        datetimeString = datetimeNow.strftime("%d-%m-%Y %H-%M-%S")
        save_path = "app/static/screenshots/"
        fileName = os.path.join(save_path, f"screenshort-{datetimeString}.png")
        image = pyscreenshot.grab()
        image.save(fileName)
        image = ""
        datetimeString = ""
        time.sleep(3)


# def test():
#   check_if_user_exists = User.objects.filter(username="username").exists()   
# if check_if_user_exists:
#     user = authenticate(request, username=username, password=password)
def loginView(request):
    # after checking if the user is active, exists and passwword matches
    request.session["isLoggedIn"] = True
    request.session["username"] = request.POST.get("username")





def login_user(request):
    global thread
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            global proc
            proc = multiprocessing.Process(target=take_screenshots, args=(username,))
            proc.start()
            return render(request, 'home.html')

        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login_user')

    else:
        return render(request, 'login.html')


def logout_user(request):
    proc.terminate()
    auth.logout(request)
    return redirect('home')
