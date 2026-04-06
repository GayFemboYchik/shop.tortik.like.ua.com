from django.urls import path, include
from .views import *
urlpatterns = [
    path('instruments/', InstrumentListView.as_view(),name="instrument_list"),
    path('instruments/<int:pk>/', InstrumentDetailView.as_view(), name="instrument_detail"),
    path('cart/', CartView.as_view(), name="cart"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
]

app_name = "instrument_shop"
