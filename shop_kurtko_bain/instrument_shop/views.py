from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *


class InstrumentListView(ListView):
    model = Instrument
    template_name = "shop/instrument_list.html"
    context_object_name = "instruments"

    def get_queryset(self):
        queryset = Instrument.objects.all()
        subcategory_id = self.request.GET.get('subcategory')
        category_id = self.request.GET.get('category')

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if subcategory_id:
            queryset = queryset.filter(subcategory_id=subcategory_id)

        return queryset

