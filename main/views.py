from django.shortcuts import render, redirect, HttpResponse
from main.models import Item
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.

def homepage(request):
    return render(request, template_name='main/home.html')

def itemspage(request):
    if request.method == 'GET':
        items = Item.objects.filter(owner=None)
        return render(request, template_name='main/items.html', context={"items": items})
    if request.method == 'POST':
        purchased_item = request.POST.get('purchased-item')
        if purchased_item:
            purchased_item_obj = Item.objects.get(name=purchased_item)
            purchased_item_obj.owner = request.user
            purchased_item_obj.save()
            messages.success(request, f"Congrats! You bought {purchased_item} for {purchased_item_obj.name}")

        return redirect('items')

def loginpage(request):
    if request.method == 'GET':
        return render(request, template_name='main/login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"You are logged in as {user.username}")
            return redirect('items')
        else:
            messages.error(request, "The combination of username and password is wrong!")
            return redirect('login')



def registerpage(request):
    if request.method == 'GET':
        return render(request, template_name='main/register.html')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f"You have registered your account successfully! Logged in as {username}")
            return redirect('home')
        else:
            messages.error(request, form.errors)
            return redirect('register')

def logoutpage(request):
    logout(request)
    messages.success(request, f"You have been logged out!")
    return redirect('home')

def orderspage(request):
    if request.user.is_authenticated:
        owned_items = Item.objects.filter(owner=request.user)
        return render(request, template_name='main/orders.html', context={'owned_items': owned_items})
    else:
        return render(request, template_name='main/orders.html')