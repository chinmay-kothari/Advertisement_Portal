import django_filters
from .models import Advertisement, Category, Subcategory, Location
from taggit.managers import TaggableManager
from dal import autocomplete
from .forms import AdvertisementFilterForm
from django import forms


class AdvertisementFilter(django_filters.FilterSet):

    category = django_filters.ModelChoiceFilter(
        widget=autocomplete.ModelSelect2(url='advertisements:categoryAutoComplete'),
        queryset=Category.objects.all()
    )
    subcategory = django_filters.ModelChoiceFilter(
        widget=autocomplete.ModelSelect2(
            url='advertisements:subcategoryAutoComplete',
            forward=('category')
        ),
        queryset=Subcategory.objects.all()
    )
    locations = django_filters.ModelMultipleChoiceFilter(
        widget=autocomplete.ModelSelect2Multiple(
            url='advertisements:locationAutoComplete'
        ),
        queryset=Location.objects.all()
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        widget=autocomplete.ModelSelect2Multiple(
            url='advertisements:tagAutoComplete'
        ),
        queryset=Advertisement.tags.all()
    )

    def __init__(self, *args, **kwargs):
        super(AdvertisementFilter, self).__init__(*args, **kwargs)

    class Meta:
        model = Advertisement
        fields = {'description': ['icontains'], 'category': ['exact'],
                  'subcategory': ['exact'], 'tags': ['exact'], 'locations': ['exact']}
