from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
import json
from .forms import *
# Create your views here.

def home(request):
    context = {}
    return render(request, 'list_manager/home.html', context)


def listView(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        userlist, created = userList.objects.get_or_create(user_id=user_id)
        items = userlist.item_set.all()
        if request.method == 'POST':
            date = request.POST.get('date')
            if date:
                items = userlist.item_set.filter(date=date)
            else:
                items = userlist.item_set.all()
    else:
        return redirect('home')
    context = {'items': items}
    return render(request, 'list_manager/index.html', context)

def itemForm(request):
    if request.user.is_authenticated:
        context = {}
    else:
        return redirect('home')
    return render(request, 'list_manager/add.html', context)

def addItem(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        user_id = request.user.id
        userlist, created = userList.objects.get_or_create(user_id=user_id)
        Item.objects.create(
            userlist=userlist,
            item_name=data['item']['item_name'],
            item_quantity=data['item']['item_quantity'],
            item_status=data['item']['item_status'],
            date=data['item']['date'],
            )
    else:
        return redirect('home')

    return redirect('listview')

def updateForm(request, pk):
    if request.user.is_authenticated:
        item = Item.objects.get(id=pk)
        item.date = str(item.date)
        context = {'item': item}
    else:
         return redirect('home')
    return render(request, 'list_manager/update.html', context)

def deleteItem(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        item_id = data['item_id']
        action = data['action']
        item = Item.objects.get(id=item_id)
        if action=='delete':
            item.delete()
        return JsonResponse('Item was deleted', safe=False)
    else:
        return redirect('home')

def updateItem(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        item_id = data['item']['url_id'].split('/')[-2]
        item = Item.objects.get(id=item_id)
        item.item_name = data['item']['item_name']
        item.item_quantity = data['item']['item_quantity']
        item.item_status = data['item']['item_status']
        item.date = data['item']['date']
        item.save()
    else:
        return redirect('home')
    return redirect('listview')


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('listview')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'list_manager/login.html', context)

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            # Added username after video because of error returning customer name if not added
            gbagUser.objects.create(
                user=user,
                name=user.username,
                email=user.email,
            )

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'list_manager/register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')