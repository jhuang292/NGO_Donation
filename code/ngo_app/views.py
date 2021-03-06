from django.shortcuts import render
from django.contrib.auth.views import LoginView , LogoutView
from django.urls import reverse_lazy
from django.views.generic import *
from django.views import View
from .models import Donation
from .models import EventRegistration,Events ,User , Group , AdminToUserMAp , AdminToEventMap
from .forms import UserDataForms
from django.shortcuts import get_object_or_404 ,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import AddUserForm
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required
import smtplib
from datetime import date
from django.forms.widgets import PasswordInput

class ListAll(ListView):
    template_name = "HomeTable.html"
    paginate_by = 10
    def get_queryset(self):
        if is_auth_perm(self.request, True):
            return User.objects.exclude(is_superuser=True)
        else:
            print(EventRegistration.objects.filter(user_user_model=self.request.user))
            return EventRegistration.objects.filter(user_user_model=self.request.user)









class UpdateUsers(UpdateView):
    model = User
    class Meta:
        widgets = {

            'password': 'PasswordInput'
        }
    fields = ['first_name', 'last_name', 'email']
    template_name = 'base.html'
    pk_url_kwarg = 'pk'
    success_url = '/'
    def get(self, request, *args, **kwargs):
        if is_auth_perm(request, True) and is_your_user(request, User.objects.get(pk=kwargs['pk'])):
            return super().get(request, args, kwargs)
        else:
            return Auth_login_or_Deny(request)

    def post(self, request, *args, **kwargs):
            if is_auth_perm(request,True) and is_your_user(request, User.objects.get(pk=kwargs['pk'])):
                return super().post(request, args, kwargs)
            else:
                return Auth_login_or_Deny(request)


class DelUser(DeleteView):
    model = User

    def get(self, request, *args, **kwargs):
        if is_auth_perm(request, True):
            try:
                pkkey = kwargs['pk']
            except:
                return HttpResponse(status=500)
            if is_your_user(request, User.objects.get(pk=pkkey)):
                user = get_object_or_404(User, pk=pkkey)
                user.delete()
                return redirect('/')
        return Auth_login_or_Deny(request)


class AddUser(CreateView):
    model = User
    fields = ['username','first_name', 'last_name', 'email', 'password']
    template_name = 'base.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if is_auth_perm(request, True):
            form = AddUserForm
            return render(request, 'base.html', {'form':form})
        else:
            return Auth_login_or_Deny(request)

    def post(self, request, *args, **kwargs):
        if is_auth_perm(request, True):
            form = AddUserForm(request.POST)
            if form.is_valid():
                ustobj = form.save()
                ustobj.groups.set([get_object_or_404(Group, name="User")])
                ustobj.save()
                AdminToUserMAp.objects.create(Admin=request.user , Non_Admin=ustobj)
                return redirect("/")
            else: return render(request, 'base.html', {'form':form})
        return Auth_login_or_Deny(request)


class AddEvent(CreateView):
    model = Events
    fields = ['name', 'type']
    template_name = 'base.html'
    success_url = '/'
    def post(self, request, *args, **kwargs):
        if is_auth_perm(request, True):
            returnrequest = super().post(request, args, kwargs)
            AdminToEventMap.objects.create(Admin=request.user, event=self.object)
            return returnrequest
        else:
            return Auth_login_or_Deny(request)

    def get(self, request, *args, **kwargs):
        if is_auth_perm(request, True):
            return super().get(request,args, kwargs)
        else:
            return Auth_login_or_Deny(request)


class UpdateEvent(UpdateView):
    model = Events
    fields = [ 'name', 'type', 'status']
    template_name = 'base.html'
    pk_url_kwarg = 'pk'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        if is_auth_perm(request, True) and is_your_event(request, Events.objects.get(pk=kwargs['pk'])):
            return super().post(request, args, kwargs)

        else:
            return Auth_login_or_Deny(request)

    def get(self, request, *args, **kwargs):
        if is_auth_perm(request, True) and is_your_event(request, Events.objects.get(pk=kwargs['pk'])):
            return super().get(request, args, kwargs)
        else:
            return Auth_login_or_Deny(request)


class DelEvent(DeleteView):
    model = Events

    def get(self, request, *args, **kwargs):
        if is_auth_perm(request, True):
            try:
                pkkey = kwargs['pk']
            except:
                return HttpResponse(status=500)
            if is_your_event(request, Events.objects.get(pk=pkkey)):
                event = get_object_or_404(Events, pk=pkkey)
                event.delete()
                return redirect('/')
        return Auth_login_or_Deny(request)

class AllEventsView(ListView):
    model = Events
    queryset = Events.objects.all()
    template_name = 'AdminTableForEvents.html'




class EvenRegistrationView(CreateView):
    model = EventRegistration
    fields = ['first_name', 'last_name', 'cma', 'phone', 'email', 'address_line1', 'address_line2', 'city','state_code', 'zip', 'country', 'urbanization']
    template_name = 'base.html'
    success_url = '/events/cart/'

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            responce = super().post(request, args, kwargs)
            self.object.user_user_model = request.user
            self.object.save()
            request.session["Registration"] = self.object.pk
            return responce
        return Auth_login_or_Deny(request)




class ListCArtView(ListView):
    queryset = Events.objects.all()
    template_name = 'CartTable.html'
    def post(self, request, *args, **kwargs):
        don_pk_list = []
        sum = 0
        itemlist = [i for i in request.POST.items()]
        don = []
        for i in range(len(itemlist)):
            item = itemlist[i]
            print(item)

            if item[0][0:9] == 'itempknum':

                don = Donation.objects.create(event=Events.objects.get(pk=int(item[0][9:])),
                                            donation_amount = safe_float_cast(item[1]), is_recurring=False ,user_data = EventRegistration.objects.get(pk=int(request.session["Registration"])))
                don.save()
                sum += safe_float_cast(item[1])
                if safe_float_cast(item[1]) != 0.0:
                    don_pk_list.append(don.pk)

            elif item[0][0:6] == 'itempk':
                Donation.objects.filter(pk=don.pk).update(is_recurring = True)
                # obj.is_recurring = True
                #


            request.session['items'] = don_pk_list
        request.session['sum']=sum
        return redirect('/Checkout/')

    def get(self, request, *args, **kwargs):
        if 'regist_pk' in kwargs.keys():
            get_object_or_404(EventRegistration, pk=kwargs['regist_pk'])
            request.session["Registration"] = kwargs['regist_pk']
        return super().get(request, args, kwargs=None)



class CartCheckout(ListView):
    model = Donation
    template_name = 'payment.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = self.get_queryset()
        return {'sum': self.request.session['sum'] ,'object_list':object_list }
    def get_queryset(self):
        return Donation.objects.filter(pk__in=[int(item) for item in self.request.session['items']])


    def post(self, request, *args, **kwargs):
        send_string = "Your total is" + str(request.session['sum']) + "from car"
        self.get_queryset().update(is_paid=True, date_dj_name=date.today())
        # send_mail(
        #     'Reciept',
        #     send_string,
        #     'david.r.dudek@gmail.com',
        #     [EventRegistration.objects.get(pk=request.session['Registration']).email] ,
        #     fail_silently=False,
        # )

        don = Donation.objects.filter(pk__in=list(request.session['items']))
        for i in don:
            don.date_dj_name = date.today
            don.is_paid = True

        del request.session['items']
        del request.session['Registration']
        del request.session['sum']

        return redirect("/")




class ListDonations(ListView):
    #paginate_by = 10
    queryset = Donation.objects.all()
    template_name = "AdminTableForDonations.html"



def is_perm(request, is_Admin=False ):
        if is_Admin:
            temp = Group.objects.get(name='Admin')
            if temp in list(request.user.groups.all()):
                return True
            else: return False
        else:
            temp = Group.objects.get(name='User')
            if temp in list(request.user.groups.all()):
                return True
            else:
                return False


class ProccessPayment(CreateView):
    pass


def is_auth_perm(request, is_Admin =False):
    if request.user.is_authenticated:
        return is_perm(request, is_Admin)
    else:
        return False

def Auth_login_or_Deny(request):
    if request.user.is_authenticated:
        return render(request, 'accessDenied.html')
    return redirect('/login')

def is_your_user(request , user):
    return user in [item.Non_Admin for item in list(AdminToUserMAp.objects.filter(Admin=request.user))] or user == request.user

def is_your_event(request, event):
    return event in [item.event for item in AdminToEventMap.objects.filter(Admin=request.user)]

def safe_float_cast(variable):
    try:
        return float(variable)
    except:
        print('Cannot cast flaot-in reall deployment this would go to log ')
        return 0.0

