from dataclasses import fields
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView, View
from django.views.generic.base import TemplateView
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect 
from django.urls import reverse
from .models import Product, Customer, Order, OrderItem, CheckoutAddress
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt

# Auth imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CheckoutForm

# import stripe
# stripe.api_key = settings.STRIPE_KEY

# Create your views here.
class Home(TemplateView):
    template_name = 'home.html'

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

class Product_Detail(DetailView):
    model = Product
    template_name="product_detail.html"
    def get_context_data(self, *args, **kwargs):
        context = super(Product_Detail, self).get_context_data(*args, **kwargs)
        product = get_object_or_404(Product, id=self.kwargs['pk'])
        return context

class Product_List(TemplateView):
    template_name = 'product_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context['cat'] = ['Armor', 'Books', 'Food', 'Jewelery', 'Potions', 'Weapons']
        if name != None:
            context["products"] = Product.objects.filter(name__icontains=name)
            context["header"] = f"Searching for {name}"
        else:
            # if 'Armor' in self.request.POST:
            #     context['products'] = Product.objects.all.filter(name="Armor")
            # elif 'Books' in self.request.POST:
            #     context['products'] = Product.objects.all.filter(name="Books")
            # elif 'Food' in self.request.POST:
            #     context['products'] = Product.objects.all.filter(name="Food")
            # elif 'Jewelery' in self.request.POST:
            #     context['products'] = Product.objects.all.filter(name="Jewelery")
            # elif 'Potions' in self.request.POST:
            #     context['products'] = Product.objects.all.filter(name="Potions")
            # elif 'Weapons' in self.request.POST:
            #     context['products'] = Product.objects.all.filter(name="Weapons")
            # else:
            context['products'] = Product.objects.all() 
            context['header'] = "Our Products"
        return context

class Armor_List(TemplateView):
    template_name = 'armor_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context['cat'] = ['Armor', 'Books', 'Food', 'Jewelery', 'Potions', 'Weapons']
        context["products"] = Product.objects.filter(category="Armor")
        return context

class Book_List(TemplateView):
    template_name = 'book_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context['cat'] = ['Armor', 'Books', 'Food', 'Jewelery', 'Potions', 'Weapons']
        context["products"] = Product.objects.filter(category="Books")
        return context

class Food_List(TemplateView):
    template_name = 'food_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context['cat'] = ['Armor', 'Books', 'Food', 'Jewelery', 'Potions', 'Weapons']
        context["products"] = Product.objects.filter(category="Food")
        return context

class Jewelery_List(TemplateView):
    template_name = 'jewelery_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context['cat'] = ['Armor', 'Books', 'Food', 'Jewelery', 'Potions', 'Weapons']
        context["products"] = Product.objects.filter(category="Jewelery")
        return context

class Potions_List(TemplateView):
    template_name = 'potions_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context['cat'] = ['Armor', 'Books', 'Food', 'Jewelery', 'Potions', 'Weapons']
        context["products"] = Product.objects.filter(category="Potions")
        return context

class Weapons_List(TemplateView):
    template_name = 'weapons_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context['cat'] = ['Armor', 'Books', 'Food', 'Jewelery', 'Potions', 'Weapons']
        context["products"] = Product.objects.filter(category="Weapons")
        return context

@login_required
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
            return redirect("product_detail", pk = pk)
        else:
            order.items.add(order_item)
            messages.info(request, "Item added to your cart")
            return redirect("product_detail", pk = pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to your cart")
        return redirect("product_detail", pk = pk)

@login_required
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
            messages.info(request, "Item \""+order_item.item.name+"\" remove from your cart")
            return redirect("product_detail", pk=pk)
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("product_detail", pk=pk)
    else:
        #add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("product_detail", pk = pk)

# class OrderItem_List(TemplateView):
#     template_name = 'cart.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         name = self.request.GET.get("name")
#         if name != None:
#             context["order"] = Order.objects.get(user=self.request.user, ordered=False)
#             context["products"] = Product.objects.filter(name__icontains=name)
#             context["header"] = f"Searching for {name}"
#         else: 
#             context['products'] = Product.objects.all() 
#             context['header'] = "Our Products"
#         return context

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'cart2.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("/")

@login_required
def subtract_item(request, pk):
    item = get_object_or_404(Product, pk=pk )
    order_qs = Order.objects.filter(
        user = request.user, 
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists() :
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, "Item quantity was updated")
            return redirect("cart")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("cart")
    else:
        messages.info(request, "You do not have an Order")
        return redirect("cart")

@login_required
def add_item(request, pk):
    item = get_object_or_404(Product, pk=pk )
    order_qs = Order.objects.filter(
        user = request.user, 
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists() :
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            if order_item.quantity < order_item.item.quantity:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "Item quantity was updated")
            else:
                messages.info(request, "Store doesn't have that many in stock")
            return redirect("cart")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("cart")
    else:
        messages.info(request, "You do not have an Order")
        return redirect("cart")

class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                same_billing_address = form.cleaned_data.get('same_billing_address')
                save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')

                checkout_address = CheckoutAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                checkout_address.save()
                order.checkout_address = checkout_address
                order.save()
                return redirect('pickup')
            messages.warning(self.request, "Failed Chekout")
            return redirect('checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("cart")

class Pickup(TemplateView):
    template_name = 'pickup.html'

# class PaymentView(View):
#     def get(self, *args, **kwargs):
#         order = Order.objects.get(user=self.request.user, ordered=False)
#         context = {
#             'order': order
#         }
#         return render(self.request, "payment.html", context)

#     def post(self, *args, **kwargs):
#         order = Order.objects.get(user=self.request.user, ordered=False)
#         token = self.request.POST.get('stripeToken')
#         amount = int(order.get_total_price() * 100)  #cents

#         try:
#             charge = stripe.Charge.create(
#                 amount=amount,
#                 currency="usd",
#                 source=token
#             )

#             # create payment
#             payment = Payment()
#             payment.stripe_id = charge['id']
#             payment.user = self.request.user
#             payment.amount = order.get_total_price()
#             payment.save()

#             # assign payment to order
#             order.ordered = True
#             order.payment = payment
#             order.save()

#             messages.success(self.request, "Success make an order")
#             return redirect('/')

#         except stripe.error.CardError as e:
#             body = e.json_body
#             err = body.get('error', {})
#             messages.error(self.request, f"{err.get('message')}")
#             return redirect('/')

#         except stripe.error.RateLimitError as e:
#             # Too many requests made to the API too quickly
#             messages.error(self.request, "To many request error")
#             return redirect('/')

#         except stripe.error.InvalidRequestError as e:
#             # Invalid parameters were supplied to Stripe's API
#             messages.error(self.request, "Invalid Parameter")
#             return redirect('/')

#         except stripe.error.AuthenticationError as e:
#             # Authentication with Stripe's API failed
#             # (maybe you changed API keys recently)
#             messages.error(self.request, "Authentication with stripe failed")
#             return redirect('/')

#         except stripe.error.APIConnectionError as e:
#             # Network communication with Stripe failed
#             messages.error(self.request, "Network Error")
#             return redirect('/')

#         except stripe.error.StripeError as e:
#             # Display a very generic error to the user, and maybe send
#             # yourself an email
#             messages.error(self.request, "Something went wrong")
#             return redirect('/')
        
#         except Exception as e:
#             # Something else happened, completely unrelated to Stripe
#             messages.error(self.request, "Not identified error")
#             return redirect('/')