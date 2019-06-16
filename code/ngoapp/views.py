from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView


@method_decorator(csrf_exempt, name='dispatch')
class BaseView(View):
    def get(self, request):
        # <view logic>
        return render(request, 'PostTest.html')

    # def post(self, request):
    #    # if request.post == "true" this is non-sense but its just a reminder
    #     return render(request, 'trialbase.html')
    #

#class ReturnList(UpdateView):

