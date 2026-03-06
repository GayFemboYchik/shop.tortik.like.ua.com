from django.urls import path, include
from .views import *
urlpatterns = [
    path('instruments/', InstrumentListView.as_view()),
]
