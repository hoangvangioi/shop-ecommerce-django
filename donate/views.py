from django.shortcuts import render
from .models import Donate
from django.views.generic import ListView


# Create your views here.


class DonateListView(ListView):
    model = Donate
    context_object_name = "donates"
    template_name = "donate/donate.html"