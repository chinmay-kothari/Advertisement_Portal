from django.urls import path

from .views import (
    MyAdvertisementsView,
    MyAdvertisementsDetailView,
    MyAdvertisementDeleteView,
    homeView,
    redirectToProductPage,
    TagAutoComplete,
    LocationAutoComplete,
    CategoryAutoComplete,
    SubcategoryAutoComplete,
    support,
    ajax_test
)

app_name = "advertisement"
urlpatterns = [
    path("", homeView.as_view(), name="home"),
    path("my-advertisements/", view=MyAdvertisementsView.as_view(), name="myAdvertisements"),
    path("my-advertisements/<int:pk>/", view=MyAdvertisementsDetailView.as_view(), name="myAdvertisementUpdate"),
    path("my-advertisements/delete/<int:pk>/", view=MyAdvertisementDeleteView.as_view(), name="myAdvertisementDelete"),

    path("product-page/<int:pk>/", view=redirectToProductPage, name="productPage"),

    path("tag-autocomplete/", view=TagAutoComplete.as_view(), name="tagAutoComplete"),
    path("location-autocomplete/", view=LocationAutoComplete.as_view(), name="locationAutoComplete"),
    path("category-autocomplete/", view=CategoryAutoComplete.as_view(), name="categoryAutoComplete"),
    path("subcategory-autocomplete/", view=SubcategoryAutoComplete.as_view(), name="subcategoryAutoComplete"),
    path("support/", support, name="support"),
    path("ajax_test/", ajax_test, name="ajax_test"),

]
