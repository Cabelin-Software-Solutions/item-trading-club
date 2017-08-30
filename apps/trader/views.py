# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import Item, Proposal, Log
from django.db.models import Q
from .forms import LoginForm, RegisterForm, ItemForm, DeleteItemForm, EditItemForm, EditUserForm, ChangePasswordForm, AlertForm
from django.contrib.auth.models import User


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
                owner=request.user,
                in_sender_trade=False)
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
    items = Item.objects.all().exclude(owner=request.user.id)
    return render(request, 'market.html', {
        'items': items
    })


@login_required
def trade_view(request):
    # use filters
    sent_proposals = Proposal.objects.filter(sender=request.user).exclude(status="Complete").exclude(status="Cancelled").exclude(status="Rejected")
    received_proposals = Proposal.objects.filter(receiver=request.user).exclude(status="Complete").exclude(status="Cancelled").exclude(status="Rejected")
    completed_proposals = Proposal.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).filter(status="Complete")
    context = {
        'received_proposals' : received_proposals,
        'sent_proposals' : sent_proposals,
        'completed_proposals': completed_proposals
    }
    return render(request, 'trades.html', context)

@login_required
def trade_request_view(request):
    if request.method == "POST":
        # get receiver_item object based on item id
        rec_item = Item.objects.get(pk=request.POST['item_id'])
        if rec_item.in_sender_trade == True:
            return HttpResponseRedirect("/market?error=Item is currently being traded by the owner")
        rec = rec_item.owner

        # create default item
        try:
            default_item = Item.objects.get(name="No item in trade")
        except:
            default_item = Item.objects.create(name="No item in trade", description="None", image="None",in_sender_trade=False)

        # create proposal object
        proposal = Proposal(status="Pending",sender=request.user,sender_item=default_item,receiver=rec,receiver_item=rec_item,is_finalized=False)
        proposal.save()
        trade_id = str(proposal.id)
    return HttpResponseRedirect("/item/trade/"+ trade_id +"/window?message=Successfully created a trade request")

@login_required
def trade_window_view(request, trade_id):
    proposal = Proposal.objects.get(pk=trade_id)
    if request.user.id == proposal.sender.id or request.user.id == proposal.receiver.id:
        if not proposal.sender_item or not proposal.receiver_item:
            return HttpResponseRedirect("/trades/?error=Invalid Proposal. Either proposal may have been completed, and items have changed owners, or an error has been encountered in the trade request")

        current_user = request.user
        sender_items = Item.objects.filter(owner=proposal.sender).filter(in_sender_trade=False)
        context = {
            'user'            : current_user,
            'proposal'        : proposal,
            'avail_items'     : sender_items,
            'message'         : request.GET.get('message'),
            'error'           : request.GET.get('error')

        }

        return render(request, "trade_window.html", context)
    return HttpResponseRedirect("/trades/?error=Unauthorized Access")

@login_required
def trade_update_view(request, trade_id):
    if request.method == "POST":
        proposal = Proposal.objects.get(pk=trade_id)
        if not proposal.sender_item or not proposal.receiver_item:
            return HttpResponseRedirect("/trades/?error=Invalid Proposal. Either proposal may have been completed, and items have changed owners, or an error has been encountered in the trade request")

        if proposal.status != 'Cancelled':
            if proposal.is_finalized == False:
                new_trade_item = Item.objects.get(pk=request.POST['item'])
                proposal.sender_item.in_sender_trade = False
                proposal.sender_item.save()
                proposal.sender_item = new_trade_item
                proposal.save()
                proposal.sender_item.in_sender_trade = True
                proposal.sender_item.save()
                return HttpResponseRedirect("/item/trade/"+ trade_id +"/window?message=Successfully updated your trade request")
            else:
                return HttpResponseRedirect("/item/trade/"+ trade_id +"/window?error=Cannot update a finalized trade request")

    return HttpResponseRedirect("/item/trade/"+ trade_id +"/window?error=Something went wrong")

@login_required
def trade_finalize_view(request, trade_id):
    if request.method == "POST":
        proposal = Proposal.objects.get(pk=trade_id)
        if not proposal.sender_item or not proposal.receiver_item:
            return HttpResponseRedirect("/trades/?error=Invalid Proposal. Either proposal may have been completed, and items have changed owners, or an error has been encountered in the trade request")
        if proposal.status != 'Cancelled':
            if proposal.sender_item.name != 'No item in trade':
                proposal.is_finalized = True
                proposal.status = "Finalized"
                proposal.save()
                return HttpResponseRedirect("/item/trade/"+ trade_id +"/window?message=Finalized your trade request")
            else:
                return HttpResponseRedirect("/item/trade/"+ trade_id +"/window?error=Please offer an item to trade")

    return HttpResponseRedirect("/item/trade/"+ trade_id +"/window?error=Something went wrong")

@login_required
def trade_cancel_view(request, trade_id):
    if request.method == "POST":
        proposal = Proposal.objects.get(pk=trade_id)
        if not proposal.sender_item or not proposal.receiver_item:
            return HttpResponseRedirect("/trades?error=Invalid Proposal. Either proposal may have been completed, and items have changed owners, or an error has been encountered in the trade request")
        proposal.sender_item.in_sender_trade = False
        proposal.sender_item.save()
        proposal.is_finalized = False
        proposal.status = "Cancelled"
        proposal.save()
        return HttpResponseRedirect("/trades?message=You cancelled your trade request")
    return HttpResponseRedirect("/item/trade/"+ trade_id +"/window?error=Something went wrong")



@login_required
def trade_accept_view(request, trade_id):
    if request.method == "POST":
        proposal = Proposal.objects.get(pk=trade_id)
        if proposal.status != 'Cancelled':
            if proposal.is_finalized:
                rec_item = proposal.receiver_item
                rec_item.owner = proposal.sender
                rec_item.save()
                rec_item.item_receive_proposals.clear()
                rec_item.item_send_proposals.clear()

                sen_item = proposal.sender_item
                sen_item.owner = proposal.receiver
                sen_item.save()
                sen_item.item_receive_proposals.clear()
                sen_item.item_send_proposals.clear()

                proposal.status = "Complete"
                proposal.save()

                log_message = proposal.sender.first_name + " " + proposal.sender.last_name + " completed a trade request with " + proposal.receiver.first_name + " " + proposal.receiver.last_name
                log = Log.objects.create(message=log_message, trade=proposal)
                return HttpResponseRedirect("/trades?message=Trade Complete")
            else:
                return HttpResponseRedirect("/item/trade/"+ trade_id +"/window?error=Trade must be finalized by the Sender")
    return HttpResponseRedirect("/item/trade/"+ trade_id +"/window?error=Something went wrong")

@login_required
def trade_reject_view(request, trade_id):
    if request.method == "POST":
        proposal = Proposal.objects.get(pk=trade_id)
        if proposal.status != 'Cancelled':
            proposal.sender_item.in_sender_trade = False
            proposal.sender_item.save()
            proposal.is_finalized = False
            proposal.status = "Rejected"
            proposal.save()
            return HttpResponseRedirect("/trades?message=Trade Rejected")
    return HttpResponseRedirect("/item/trade/"+ trade_id +"/window?error=Something went wrong")
