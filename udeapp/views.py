from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def loginpage(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                messages.success(request, ("Loged in successfully"))
                return redirect('home')
            else:
                messages.success(request, ("Invalid username or password"))
                return redirect('login_page')
        else:
            return render(request, 'loginpage.html')
    else:
        return redirect('home')

def homepage(request):
    if request.user.is_authenticated:
        return render(request, 'index.html', {})
    else:
        return redirect('login_page')

def view_user(request):
    if request.user.is_superuser or request.user.is_staff:
        users = User.objects.all()
        return render(request, 'viewuser.html', {"users":users})
    else:
        return redirect('home')

def createUser(request):
    if request.user.is_superuser or request.user.is_staff:
        if request.method == 'POST':
            username_in = request.POST['username']
            if not username_in == '' :
                if not User.objects.filter(username = username_in):
                    email = request.POST['email']
                    firstname_in = request.POST['first_name']
                    lastname_in = request.POST['last_name']
                    if request.POST['password1'] == request.POST['password2'] and not request.POST['password1']  == '':
                        password_in = request.POST['password1']
                        user_entery = User.objects.create_user(username_in, email, password_in)
                        user_entery.first_name = firstname_in
                        user_entery.last_name = lastname_in
                        user_entery.save()
                        messages.success(request, ("User created"))
                        return redirect('home')
                    else:
                        messages.success(request, ("Password does not match"))
                        return render(request, 'creat.html')
                else:
                    messages.success(request, ("Username already exist"))
                    return render(request, 'creat.html')
            else:
                messages.success(request, ("Username must be provided"))
                return render(request, 'creat.html')
        else:
            return render(request, 'creat.html')
    else:
        messages.success(request, ("Only Staffs are alowed"))
        return redirect('home')

def editUser(request, user_id):
    if request.user.is_superuser or request.user.is_staff:
            if request.method == 'POST':
                edit_user = User.objects.get(pk = user_id)
                username_in = request.POST['username']
                if not username_in == '' :
                    if not User.objects.filter(username = username_in) or edit_user.username == username_in:
                        email = request.POST['email']
                        firstname_in = request.POST['first_name']
                        lastname_in = request.POST['last_name']
                        if request.POST['password1'] == request.POST['password2'] and not request.POST['password1']  == '':
                            password_in = request.POST['password1']
                            edit_user.username = username_in
                            edit_user.email = email
                            edit_user.set_password = password_in
                            edit_user.first_name = firstname_in
                            edit_user.last_name = lastname_in
                            edit_user.save()
                            messages.success(request, ("User edited successfully"))
                            return redirect('home')
                        else:
                            messages.success(request, ("Password does not match"))
                            return render(request, 'edit.html')
                    else:
                        messages.success(request, ("Username already exist"))
                        return render(request, 'edit.html')
                else:
                    messages.success(request, ("Username must be provided"))
                    return render(request, 'edit.html')
            else:
                user_data = User.objects.get(pk=user_id)
                return render(request, 'edit.html', {"details":user_data})
    else:
        return redirect('home')

def deletUser(request, user_id):
    if request.user.is_superuser or request.user.is_staff:
        userdelete = User.objects.get(pk = user_id)
        if userdelete.is_superuser:
            messages.success(request, ("You can't delet super user"))
            return redirect('home')
        else:
            userdelete.delete()
            messages.success(request, ("User deleted"))
            return redirect('home')
    else:
        return redirect('login_page')

def search_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST['searched'] == '':
                messages.success(request, ("You didn't search any users"))
                return redirect('home')
            else:
                user = request.POST['searched']
                searched_items = User.objects.filter(username__contains = user)
                return render(request, 'searched.html', {"items":searched_items})
        else:
            return redirect('home')
    else:
        return redirect('login_page')
        

def logout_user(request):
    logout(request)
    return redirect('login_page')
