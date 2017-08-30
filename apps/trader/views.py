# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import LoginForm, RegisterForm, ItemForm, DeleteItemForm, EditItemForm, EditUserForm, ChangePasswordForm, AlertForm
from django.contrib.auth.models import User
from .models import Item

# Create your views here.
def index(request):
    login_form = LoginForm()
    register_form = RegisterForm()
    return render(request, 'index.html', {
                'login_form': login_form,
                'register_form': register_form,
                'message': request.GET.get('message'),
                'error': request.GET.get('error')
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
    if request.method == 'POST':
        pass
    else:
        user = User.objects.get(id = request.user.id)
        edit_profile_form = EditUserForm({'username':user.username,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email
        })
        password_form = PasswordChangeForm(request)
        return render(request, 'profile.html', {
            'form': edit_profile_form,
            'password_form': password_form,
            'message': request.GET.get('message'),
            'error': request.GET.get('error')
        })

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            user = User.objects.get(id = request.user.id)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            return HttpResponseRedirect('/profile?message=Successfully changed profile info')
        else:
            return HttpResponseRedirect('/profile?error=Error editing password')

@login_required
def password_edit_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect('/profile?message=Successfully changed password')
        else:
            return HttpResponseRedirect('/profile?error=Error changing password')

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
        items = Item.objects.filter(owner=request.user).order_by('-updated_at')
        item_form = ItemForm()
        delete_form = DeleteItemForm()
        return render(request, 'my_items.html', {
            'item_form': item_form,
            'delete_form': delete_form,
            'items': items
        })

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
        try:
            item = Item.objects.get(id = item_id, owner = request.user.id)
            item_form = EditItemForm({'id':item_id,'name':item.name, 'description':item.description, 'image':item.image})
            return render(request, 'edit_item.html', {
                'item_form': item_form
                })
        except:
            return HttpResponseRedirect('/my_items?error=Item not found')

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
