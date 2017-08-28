# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

# Create your views here.
def index(request):
    login_form = LoginForm()
    register_form = UserCreationForm()
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
        form = UserCreationForm(request.POST)
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
    return render(request, 'my_items.html')

@login_required
def market_view(request):
    return render(request, 'market.html')
