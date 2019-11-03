# from django.shortcuts import render
from dal import autocomplete
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from adverge.advertisements.models import Advertisement, Location, Category, Subcategory, Stats, WeeklyStats, Support
from adverge.advertisements.forms import AdvertisementCreationForm
from django.http import HttpResponse
from .filters import AdvertisementFilter
from paypal.standard.forms import PayPalPaymentsForm
from django.shortcuts import redirect
from django.contrib import messages
from django.http import Http404

# def myAdvertisements(request):
#     return render(request, "advertisements/myAdvertisements.html", {})


class homeView(ListView):
    model = Advertisement
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_global'] = False
        context['minimize'] = False

        print(self.request.GET)

        if(not self.request.GET == {}):
            context['filters'] = AdvertisementFilter(self.request.GET, queryset=self.get_queryset())
            qs = context['filters'].qs

            # Total Number of times appeared in searches
            description = self.request.GET.get('description__icontains')
            if description:
                for advertisement in qs:
                    stats, created = Stats.objects.get_or_create(advertisement=advertisement)
                    stats.searches_appeared_in = stats.searches_appeared_in + 1
                    stats.save()
                    print(stats.searches_appeared_in)

            # Total Number of times appeared in tags
            tag_ids = self.request.GET.getlist('tags')
            if tag_ids:
                for advertisement in qs:
                    stats, created = Stats.objects.get_or_create(advertisement=advertisement)
                    stats.tags_appeared_in = stats.tags_appeared_in + 1
                    stats.save()
                    print(stats.tags_appeared_in)

        else:
            context['filters'] = AdvertisementFilter(queryset=self.get_queryset())
            qs = context['filters'].qs

        # Total Number of times appeared on Homepage
        for advertisement in qs:
            stats, created = Stats.objects.get_or_create(advertisement=advertisement)
            stats.homepage_appeared_in = stats.homepage_appeared_in + 1
            stats.save()

        if (self.request.GET.get("is_global") == 'true'):
            context['is_global'] = True
        if (self.request.GET.get("minimize") == 'true'):
            context['minimize'] = True

        # local trends
        qs = context['filters'].qs
        location = 'India'
        print(qs.filter(locations__name__in=[location]))
        context['local_qs'] = qs.filter(locations__name__in=[location])
        context['local_location'] = location

        return context

    # context = get_context_data()
    template_name = 'advertisements/home.html'

# @method_decorator(login_required, name='dispatch')


class MyAdvertisementsView(CreateView):
    form_class = AdvertisementCreationForm
    success_url = reverse_lazy('advertisement:myAdvertisements')
    template_name = 'advertisements/myAdvertisements.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        form.save_m2m()

        return super().form_valid(form)

   # def redirect(self, ad_name):
    #    return HttpResponse('<h1>Hiiii</h1>')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        advertisements = Advertisement.objects.filter(user=user)
        context['advertisements'] = advertisements

        return context

# @method_decorator(login_required, name='dispatch')


class MyAdvertisementsDetailView(UpdateView):
    form_class = AdvertisementCreationForm
    model = Advertisement
    success_url = reverse_lazy('advertisement:myAdvertisements')
    template_name = 'advertisements/myAdvertisements.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        form.save_m2m()

        return super().form_valid(form)

   # def redirect(self, ad_name):
    #    return HttpResponse('<h1>Hiiii</h1>')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        advertisement_id = self.kwargs.get('pk')
        print('Id Here')
        print(advertisement_id)
        advertisements = Advertisement.objects.filter(user=user)
        context['advertisements'] = advertisements

        if advertisement_id is not None:
            advertisement = Advertisement.objects.get(pk=advertisement_id)
            context['advertisement'] = advertisement

        print(self.request.build_absolute_uri(reverse('paypal-ipn')))

        # What you want the button to do.
        paypal_dict = {
            "business": "receiver_email@example.com",
            "amount": "10.00",
            "item_name": "name of the item",
            "invoice": "1233213212132",
            "notify_url": self.request.build_absolute_uri(reverse('paypal-ipn')),
            "return": self.request.build_absolute_uri(reverse('advertisements:myAdvertisements')),
            "cancel_return": self.request.build_absolute_uri(reverse('advertisements:myAdvertisements')),
            "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
        }

        # Create the instance.
        paypal_form = PayPalPaymentsForm(initial=paypal_dict)
        context['paypal_form'] = paypal_form

        return context


class MyAdvertisementDeleteView(DeleteView):
    model = Advertisement
    success_url = reverse_lazy('advertisement:myAdvertisements')

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        if self.object.user == self.request.user:
            self.object.delete()


class TagAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class LocationAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Location.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class CategoryAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Category.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class SubcategoryAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        qs = Subcategory.objects.all()

        category = self.forwarded.get('category', None)

        if category:
            qs = qs.filter(category=category)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


def redirectToProductPage(request, pk):
    advertisement = Advertisement.objects.get(pk=pk)

    stats, created = Stats.objects.get_or_create(advertisement=advertisement)
    stats.clicks_product_page = stats.clicks_product_page + 1
    stats.save()
    print(stats.clicks_product_page)

    return redirect(advertisement.product_page_link)


def support(request):
    if request.POST:
        print(request.POST)
        obj = request.POST
        support_obj = Support.objects.create(email=obj["email"], query=obj["query"])
        print(support_obj)

        message = ("Successfully Saved you Query!")
        messages.add_message(request, messages.INFO, message)

    return redirect('advertisements:myAdvertisements')


def ajax_test(request):
    """
    View function to handle Ajax request for image Link.
    :param request: Ajax request data.
    :return: image URL.
    """
    if request.is_ajax():
        try:
            username = request.POST['username']
            # perform operations on the user name.

        except:
            e = sys.exc_info()
            return HttpResponse(e)
        return HttpResponse("< h1 > hi < /h1 >")
    else:
        raise Http404
