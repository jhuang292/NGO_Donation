from django.shortcuts import render
from django.contrib.auth.views import LoginView , LogoutView
from django.urls import reverse_lazy
from django.views.generic import *
from django.views import View
from .models import Donation
from .models import EventRegistration,Events ,User , Group
from .forms import UserDataForms
from django.shortcuts import get_object_or_404 ,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import AddUserForm
from django.core.serializers import serialize

# Create your views here.
class HomeView(LoginView, LogoutView):
    pass



class ListAll(ListView):
    queryset = User.objects.all()
    template_name = "AdminTable.html"


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
    slug_url_kwarg = 'first_name'
    slug_field = 'First Name'
    success_url = '/admin'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, args, kwargs)
        return redirect('/login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().post(request, args, kwargs)
        return redirect('/login')

class DelUser(DeleteView):
    model = User

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                pkkey = kwargs['pk']
            except:
                return HttpResponse(status=500)

            user = get_object_or_404(User, pk=pkkey)
            user.delete()
            return redirect('/admin/')



class AddUser(View):
    model = User
    fields = ['username','first_name', 'last_name', 'email', 'password']
    template_name = 'base.html'
    success_url = '/admin'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = AddUserForm
            return render(request, 'base.html', {'form':form})
        return redirect('/login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = AddUserForm(request.POST)
            super(AddUserForm, form).clean()
            ustobj = form.save()
            ustobj.groups.set([get_object_or_404(Group, name="User")])
            ustobj.save()
            return redirect("/admin/")
        return redirect('/login')



class AddEvent(CreateView):
    model = Events
    fields = ['name', 'type', 'status']
    template_name = 'base.html'
    success_url = '/admin/'

class UpdateEvent(UpdateView):
    model = Events
    fields = ['name', 'type', 'status']
    template_name = 'base.html'
    pk_url_kwarg = 'pk'
    success_url = '/admin'


class DelEvent(DeleteView):
    model = Events

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                pkkey = kwargs['pk']
            except:
                return HttpResponse(status=500)

            evnt = get_object_or_404(Events, pk=pkkey)
            evnt.delete()
            return redirect('/admin/')

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
        return render(request , "accessDeney.html")




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



