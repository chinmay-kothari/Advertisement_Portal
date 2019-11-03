from dal import autocomplete
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from adverge.advertisements.models import Advertisement, Location, Category, Subcategory
from adverge.advertisements.forms import AdvertisementCreationForm
from django.http import HttpResponse
from django.shortcuts import render
from adverge.advertisements.models import *
from django.views.generic import ListView
# def myAdvertisements(request):
#     return render(request, "advertisements/myAdvertisements.html", {})

def home(request):
	all_advertisements = Advertisement.objects.all()
	return render(request, 'pages/home.html', {'advertisements': all_advertisements})

class homeView(ListView):
    model = Advertisement
    paginate_by = 100
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_global'] = True
        context['minimize'] = True
        return context

    #context = get_context_data()
    template_name = 'pages/home.html'