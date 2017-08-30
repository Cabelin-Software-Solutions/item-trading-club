# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import LoginForm, RegisterForm, ItemForm, DeleteItemForm, EditItemForm
from .models import Item

# Create your views here.
def index(request):
    login_form = LoginForm()
    register_form = RegisterForm()
    message = request.GET.get('message')
    error = request.GET.get('error')
    return render(request, 'index.html', {
                'login_form': login_form,
                'register_form': register_form,
                'message': message,
                'error': error
            })

# authentication views
def register_view(request):
    print request
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            u = form.cleaned_data['username']
            raw_p = form.cleaned_data['password1']
            user = authenticate(username=u, password=raw_p)
            login(request, user)
            return HttpResponseRedirect('/?message=Successfully signed up')
        else:
            return HttpResponseRedirect('/?error=Form is not valid')
    else:
        return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponseRedirect('/?error=Account has been disabled')
            else:
                return HttpResponseRedirect('/?error=Username and/or Password incorrect')
        else:
            return HttpResponseRedirect('/?error=Form is not valid')
    else:
        return HttpResponseRedirect('/')

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required
def my_items_view(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = Item(name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                image=form.cleaned_data['image'],
                owner=request.user)
            item.save()
            return HttpResponseRedirect('/my_items')
    else:
        items = Item.objects.filter(owner=request.user)
        item_form = ItemForm()
        delete_form = DeleteItemForm()
        return render(request, 'my_items.html', {
            'item_form': item_form,
            'delete_form': delete_form,
            'items': items
        })

@login_required
def item_add_view(request):
    pass

@login_required
def item_edit_view(request):
    if request.method == 'POST':
        form = EditItemForm(request.POST)
        if form.is_valid():
            item_id = form.cleaned_data['id']
            i = Item.objects.get(id=item_id, owner=request.user)
            if i:
                i.name = form.cleaned_data['name']
                i.description = form.cleaned_data['description']
                i.image = form.cleaned_data['image']
                i.save()
                item_id = str(item_id)
                return HttpResponseRedirect('/my_items')
            else:
                return HttpResponseRedirect('/item/edit?id=' + item_id + '&error=Item not found')

    else:
        item_id = request.GET.get('id')
        item = Item.objects.get(id = item_id, owner = request.user.id)
        print item.name
        item_form = EditItemForm({'id':item_id,'name':item.name, 'description':item.description, 'image':item.image})
        return render(request, 'edit_item.html', {
            'item_form': item_form
            })

@login_required
def item_delete_view(request):
    if request.method == 'POST':
        form = DeleteItemForm(request.POST)
        if form.is_valid():
            item_id = form.cleaned_data['id']
            i = Item.objects.get(id = item_id)
            i.delete()
            return HttpResponseRedirect('/my_items')
    else:
        return HttpResponseRedirect('/')

@login_required
def market_view(request):
    items = Item.objects.all()
    return render(request, 'market.html', {
        'items': items
    })
