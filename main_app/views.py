from dataclasses import fields
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views import View # View class to handle requests
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect # This is our responses
from django.urls import reverse
from .models import Product, Customer, Order, OrderItem
from django.contrib.auth.models import User
# Auth imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.
class Home(TemplateView):
    template_name = 'home.html'


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

class Product_List(TemplateView):
    template_name = 'product_idx.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #this gets the name query parameter to access it 
        name = self.request.GET.get("name")
        #if the query exists we will filter by name
        if name != None:
            # .filter is the sql WHERE statement and name__icontains is doing a search for any name that contains the query param
            context["products"] = Product.objects.filter(name__icontains=name)
            context["header"] = f"Searching for {name}"
        else: 
            context['products'] = Product.objects.all() # this is where we add the key into our context object for the view to use
            context['header'] = "Our Products"
        return context

class Product_Detail(DetailView):
    model = Product
    template_name="product_detail.html"
    def get_context_data(self, *args, **kwargs):
        context = super(Product_Detail, self).get_context_data(*args, **kwargs)
        product = get_object_or_404(Product, id=self.kwargs['pk'])
        return context

@method_decorator(login_required, name='dispatch')
class Product_Update(UpdateView):
    model = Product
    fields = ['quantity']
    template_name = "product_update.html"
    def get_success_url(self):
        return reverse('product_detail', kwargs={'pk': self.object.pk})

