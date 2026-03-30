from django.urls import path, include
from .views import *
urlpatterns = [
    path('instruments/', InstrumentListView.as_view()),
]
path("login/", CustomLoginView.as_view(), name="login"),
path("logout/", CustomLogoutView.as_view(), name="logout"),
path("register/", RegisterView.as_view(), name="register"),