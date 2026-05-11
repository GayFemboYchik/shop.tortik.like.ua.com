from django.contrib.auth import login
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm


class IndexView(ListView):
    model = Instrument
    template_name = 'shop/index.html'
    context_object_name = 'recommended_instruments'

    def get_queryset(self):
        # Отримуємо 10 випадкових товарів
        return Instrument.objects.order_by('?')[:10]


class CategoryListView(ListView):
    model = Category
    template_name = 'shop/category_list.html'  # Перевірте шлях до вашої папки з шаблонами
    context_object_name = 'categories'


class InstrumentListView(ListView):
    model = Instrument
    template_name = "shop/instrument_list.html"
    context_object_name = "instruments"
    paginate_by = 12  # Додамо пагінацію для зручності

    def get_queryset(self):
        queryset = Instrument.objects.all()

        # Отримуємо слаги з URL
        category_slug = self.kwargs.get('category_slug')
        subcategory_slug = self.kwargs.get('subcategory_slug')

        if subcategory_slug:
            # Фільтруємо за підкатегорією
            queryset = queryset.filter(subcategory__slug=subcategory_slug)
        elif category_slug:
            # Фільтруємо за головною категорією
            queryset = queryset.filter(subcategory__category__slug=category_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаємо активну категорію в шаблон для заголовків
        if self.kwargs.get('subcategory_slug'):
            context['current_title'] = get_object_or_404(Subcategory, slug=self.kwargs['subcategory_slug']).title
        elif self.kwargs.get('category_slug'):
            context['current_title'] = get_object_or_404(Category, slug=self.kwargs['category_slug']).title
        else:
            context['current_title'] = "Всі товари"
        return context


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


class CustomLoginView(LoginView):
    template_name = "shop/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = "instrument_shop:login"


class RegisterView(CreateView):
    template_name = "shop/register.html"
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse_lazy("instrument_shop:login"))


class CheckoutView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # Шукаємо замовлення користувача, яке зараз має статус 'cart'
        order = get_object_or_404(Order, client=request.user, status='cart')

        if order.items.exists():
            # Змінюємо статус на 'processing' (Обробляється)
            order.status = 'processing'
            order.save()
            # Тут можна додати логіку зменшення кількості товару на складі (in_stock), якщо потрібно

            # Після оформлення перенаправляємо на головну або сторінку "Дякуємо"
            return redirect('instrument_shop:index')

            # Якщо кошик був порожній, просто повертаємо назад
        return redirect('instrument_shop:cart')


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shop/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        # Повертаємо замовлення поточного користувача, які вже в обробці або виконані
        return Order.objects.filter(client=self.request.user).exclude(status='cart').order_by('-created_at')