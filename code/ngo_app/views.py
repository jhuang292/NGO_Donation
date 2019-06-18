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
from django.core.serializers import serialize


class ListAll(ListView):
    template_name = "HomeTable.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, args, kwargs)


    def get_queryset(self):
        if is_auth_perm(self.request, True):
            return [item.Non_Admin for item in AdminToUserMAp.objects.filter(Admin=self.request.user)]
        else:
            print("The Query SEt was called")
            return Events.objects.all()







class UpdateStuff(UpdateView):
    model = EventRegistration
    fields = ['first_name', "last_name", 'address_line1', 'address_line2', 'city', 'state_code', 'zip', 'country']
    template_name = 'base.html'
    pk_url_kwarg = 'pk'

    def post(self, request, *args, **kwargs):
        form = UserDataForms
        return render(request, "base.html", {'form': form})

class UpdateUsers(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'base.html'
    pk_url_kwarg = 'pk'
    success_url = '/admin'
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
                redirect('/admin')
        return Auth_login_or_Deny(request)


class AddUser(CreateView):
    model = User
    fields = ['username','first_name', 'last_name', 'email', 'password']
    template_name = 'base.html'
    success_url = '/admin'

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
                return redirect("/admin/")
            else: return render(request, 'base.html', {'form':form})
        return Auth_login_or_Deny(request)


class AddEvent(CreateView):
    model = Events
    fields = ['name', 'type']
    template_name = 'base.html'
    success_url = '/admin/'
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
    fields = ['name', 'type', 'status']
    template_name = 'base.html'
    pk_url_kwarg = 'pk'
    success_url = '/admin'

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
                redirect('/admin')
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
            form = UserDataForms(request.POST)
            responce = super().post(request, args, kwargs)
            request.session["Registration"] = serialize('json', EventRegistration.objects.filter(pk=form.instance.pk))
            return responce
        return render(request , "accessDenied.html")




class ListCArtView(ListView):
    queryset = Events.objects.all()
    template_name = 'CartTable.html'
    def post(self, request, *args, **kwargs):
        sum = 0
        #request.session["items"] = request.POST.items()
        print(request.session["Registration"] + "hello")
        for item in request.POST.items():
            if item[0][0:9] == 'itempknum':
               don = Donation.objects.create(event_pk=int(item[0][9:]),
                                             donation_amount = float(item[1]),
                                             user_data = request.session["Registration"].pk)
        return redirect('/events/cart/')

class CartCheckout():
    pass

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
            else: return False


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
    return user in [item.Non_Admin for item in list(AdminToUserMAp.objects.filter(Admin=request.user))]

def is_your_event(request, event):
    return event in [item.event for item in AdminToEventMap.objects.filter(Admin=request.user)]


