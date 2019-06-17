from django.shortcuts import render
from django.contrib.auth.views import LoginView , LogoutView
from django.urls import reverse_lazy
from django.views.generic import *
from django.views import View
from .forms import UserDataForms
from .models import UserData, AppUser
from .forms import UserDataForms
from django.shortcuts import get_object_or_404 ,redirect
from django.http import HttpResponse
# Create your views here.
class HomeView(LoginView, LogoutView):
    pass


class BasicAppView(View):

    def get(self,request):
        form = UserDataForms()
        return render(request, "base.html", {"form": form})


class ListAll(ListView):
    queryset = AppUser.objects.all()
    template_name = "list.html"


class UpdateStuff(UpdateView):
    model = UserData
    fields = ['first_name', "last_name", 'address_line1', 'address_line2', 'city', 'state_code', 'zip', 'country']
    template_name = 'base.html'
    pk_url_kwarg = 'pk'

    def post(self, request, *args, **kwargs):
        form = UserDataForms
        return render(request, "base.html", {'form': form})

class UpdateUsers(UpdateView):
    model = AppUser
    fields = ['first_name', 'last_name', 'email','group']
    template_name = 'base.html'
    pk_url_kwarg = 'pk'
    slug_url_kwarg = 'first_name'
    slug_field = 'First Name'
    success_url = '/admin'

class DelUser(DeleteView):
    model = AppUser

    def get(self, request, *args, **kwargs):
        try:
            pkkey = kwargs['pk']
        except:
            return HttpResponse(status=500)

        user = get_object_or_404(AppUser, pk=pkkey)
        user.delete()
        return redirect('/admin/')


class AddUser(CreateView):
    model = AppUser
    fields = ['first_name', 'last_name', 'email', 'group']
    template_name = 'base.html'
    success_url = '/admin'

    # def post(self, request, *args, **kwargs):
    #     form = BookCreateForm(request.POST
    #     if form.is_valid():
    #         book = form.save()
    #         book.save()
