from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from django.views.generic import View,TemplateView,ListView
from django.views.generic.edit import CreateView
from bwf.models import User, Bill, Friend

from django.contrib.auth.decorators import login_required
from bwf.forms import UserCreationForm, AddBillForm


import json
from django.core import serializers
import logging

logger = logging.getLogger(__name__)

class IndexView(TemplateView):
    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('home')

        return super(IndexView, self).dispatch(request, *args, **kwargs)

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(HomeView, self).get_context_data(**kwargs)
        context['friends'] = user.friend_set.all()

        owe_me = list(Bill.objects.owe_me(user))
        #insert friend name
        for each in owe_me:
            friend = Friend.objects.get(email=each['debtor'], friendof=user)
            each['friend_name'] = friend.get_full_name()
            each['friend_pk'] = friend.pk
        context['owe_me'] = json.dumps(owe_me)

        owe_them =  list(Bill.objects.owe_them(user)) 
        for each in owe_them:
            friend = Friend.objects.get(email=each['creditor'], friendof=user)
            each['friend_name'] = friend.get_full_name()
            each['friend_pk'] = friend.pk
        context['owe_them'] = json.dumps(owe_them) 

        return context

home = login_required(HomeView.as_view())

class SignupView(CreateView):
    model = User
    template_name = "registration/signup.html"
    form_class = UserCreationForm
    success_url = 'home'


class AddBillView(View):
    def post(self,request,*args, **kwargs):
        post = request.POST
        new_friends = json.loads(request.POST.get('new_friend'))
        bills = json.loads(request.POST.get('bill'))

        #add new friends if exist
        for data in new_friends:
            try:
                friend = Friend()
                friend.email = data.email
                friend.first_name = data.first_name
                friend.last_name = data.last_name
                friend.friendof = request.user

                friend.save()
            except Exception :
                logging.exception()

        #add bills 
        for data in bills:
            try:
                bill = Bill()
                bill.creditor = data.creditor
                bill.debtor = data.debtor
                bill.amount = data.amount
                bill.bill_time = data.time

                bill.save()
            except Exception :
                logging.exception()

add_bill = login_required(AddBillView.as_view())

class AddFriendView(View):
    def post(self,request,*args, **kwargs):
        data = request.POST.get('friend')
        if data: 
            try:
                friend = Friend()
                friend.email = data.email
                friend.first_name = data.first_name
                friend.last_name = data.last_name
                friend.friendof = request.user

                friend.save()

            except Exception :
                logging.exception()
            
add_friend = login_required(AddFriendView.as_view())

class BillListView(TemplateView):
    template_name = "bill_list.html"

    def get_context_data(self, **kwargs):
        context = super(BillListView, self).get_context_data(**kwargs)

        user = self.request.user

        friend = Friend.objects.get(pk=kwargs['pk'])

        bills = Bill.objects.get_by_friend(user, friend.email).values()
        total_amount = 0
        for each in bills:
            if each['creditor'] == user.email:
                each['net_amount'] = each['amount']
            else:
                each['net_amount'] = -each['amount']

            total_amount += each['net_amount']

        context['friend'] = friend
        context['bills'] = bills
        context['total_amount'] = total_amount

        return context

bill_list = login_required(BillListView.as_view())



