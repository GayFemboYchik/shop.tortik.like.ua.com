from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View




class InstrumentListView(ListView):
    model = Instrument
    template_name = "shop/instrument_list.html"
    context_object_name = "instruments"

    def get_queryset(self):
        queryset = Instrument.objects.all()
        subcategory_id = self.request.GET.get('subcategory')
        category_id = self.request.GET.get('category')

        if category_id:
            queryset = queryset.filter(subcategory__category_id=category_id)

        if subcategory_id:
            queryset = queryset.filter(subcategory_id=subcategory_id)

        return queryset


class InstrumentDetailView(DetailView):
    model = Instrument
    template_name = 'shop/instrument_detail.html'
    context_object_name = 'instrument'

    def post(self, request, *args, **kwargs):
        instrument = self.get_object()  # поточний товар
        quantity = int(request.POST.get('quantity', 1))  # кількість з форми

        # Отримуємо замовлення користувача у статусі 'cart'
        order, created = Order.objects.get_or_create(
            client=request.user,
            status='cart'
        )

        # Перевіряємо, чи вже є цей товар у кошику
        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            instrument=instrument,
            defaults={'quantity': quantity}
        )

        if not created:
            # якщо вже є, просто додаємо кількість
            order_item.quantity += quantity
            order_item.save()

        return redirect(request.path)



class CartView(LoginRequiredMixin, View):
    template_name = 'shop/cart.html'

    def get(self, request, *args, **kwargs):
        # Отримуємо поточне замовлення користувача зі статусом 'cart'
        order = Order.objects.filter(client=request.user, status='cart').first()
        items = order.items.all() if order else []

        # Підрахунок загальної суми
        total = sum(item.instrument.price * item.quantity for item in items)

        context = {
            'order': order,
            'items': items,
            'total': total
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Обробка зміни кількості або видалення товарів
        action = request.POST.get('action')
        item_id = request.POST.get('item_id')
        order_item = OrderItem.objects.get(id=item_id, order__client=request.user, order__status='cart')

        if action == 'update':
            quantity = int(request.POST.get('quantity', 1))
            if quantity > 0:
                order_item.quantity = quantity
                order_item.save()
        elif action == 'delete':
            order_item.delete()

        return redirect('cart')  # після дії оновлюємо сторінку кошика

class ProfileView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shop/profile.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user).exclude(status='cart')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client'] = self.request.user
        return context

