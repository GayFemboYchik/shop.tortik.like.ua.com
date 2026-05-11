from django.urls import path, include
from .views import *
urlpatterns = [
    # Всі товари
    path('instruments/', InstrumentListView.as_view(), name="instrument_list"),
    # Товари конкретної категорії
    path('category/<slug:category_slug>/', InstrumentListView.as_view(), name="category_instruments"),
    # Товари конкретної підкатегорії
    path('subcategory/<slug:subcategory_slug>/', InstrumentListView.as_view(), name="subcategory_instruments"),
    # Детальна сторінка
    path('instruments/<slug:slug>/', InstrumentDetailView.as_view(), name="instrument_detail"),

    path('cart/', CartView.as_view(), name="cart"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', IndexView.as_view(), name='index'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('my-orders/', OrderListView.as_view(), name='order_list'),
]

app_name = "instrument_shop"
