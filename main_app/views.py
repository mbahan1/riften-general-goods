from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.
class Home(TemplateView):
    template_name = 'home.html'


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')