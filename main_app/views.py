from dataclasses import fields
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView
from django.views.generic.base import TemplateView
from django.views import View # View class to handle requests
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect # This is our responses
from django.urls import reverse
from .models import Product, Customer, Order, OrderItem
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
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

# class Product_View(DetailView):
#     model = Product
#     template_name = "product_detail.html"

class Product_Detail(DetailView):
    model = Product
    template_name="product_detail.html"
    def get_context_data(self, *args, **kwargs):
        context = super(Product_Detail, self).get_context_data(*args, **kwargs)
        product = get_object_or_404(Product, id=self.kwargs['pk'])
        return context

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

def put_in_cart(request, pk) :
    item = get_object_or_404(Product, pk = pk )
    order_item, created = OrderItem.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False
    )
    order_qs = Order.objects.filter(user = request.user, ordered = False)

    if order_qs.exists() :
        order = order_qs[0]
        
        if order.items.filter(item__pk = item.pk).exists() :
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Added quantity Item")
            return redirect("main_app:product", pk = pk)
        else:
            order.items.add(order_item)
            messages.info(request, "Item added to your cart")
            return redirect("main_app:product", pk = pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to your cart")
        return redirect("main_app:product", pk = pk)

def takeout_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk )
    order_qs = Order.objects.filter(
        user = request.user, 
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            order_item.delete()
            messages.info(request, "Item \""+order_item.item.item_name+"\" remove from your cart")
            return redirect("main_app:product")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("main_app:product", pk=pk)
    else:
        #add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("main_app:product", pk = pk)

# class Product_Detail(DetailView):
#     model = Product
#     template_name="product_detail.html"
#     def get_context_data(self, *args, **kwargs):
#         context = super(Product_Detail, self).get_context_data(*args, **kwargs)
#         product = get_object_or_404(Product, id=self.kwargs['pk'])
#         return context

# @method_decorator(login_required, name='dispatch')
# class Product_Update(UpdateView):
#     model = Product
#     fields = ['quantity']
#     template_name = "product_update.html"
#     def get_success_url(self):
#         return reverse('product_detail', kwargs={'pk': self.object.pk})

