from django.contrib import admin
from adverge.advertisements.models import Advertisement, Location, Category, Subcategory, Support
from import_export.admin import ImportExportModelAdmin

# Register your models here.


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Advertisement._meta.fields if field.name != "id"]


admin.site.register(Advertisement, AdvertisementAdmin)


@admin.register(Location)
class LocationAdmin(ImportExportModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    pass


@admin.register(Subcategory)
class SubcategoryAdmin(ImportExportModelAdmin):
    pass


@admin.register(Support)
class SupportAdmin(ImportExportModelAdmin):
    pass
