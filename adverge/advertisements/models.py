import datetime
from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager

# Create your models here.


class Advertisement(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    description = models.CharField(max_length=50)
    product_page_link = models.URLField(blank=True, max_length=5000)

    video = models.FileField()
    category = models.ForeignKey(
        'Category',
        null=True,
        on_delete=models.CASCADE,
    )
    subcategory = models.ForeignKey(
        'Subcategory',
        null=True,
        on_delete=models.CASCADE,
    )
    is_global = models.BooleanField(default=False)
    locations = models.ManyToManyField('Location', blank=True)
    tags = TaggableManager()
    validity = models.IntegerField()
    thumbnail = models.FileField()
    cost = models.IntegerField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        db_table = "advertisement"

    def __str__(self):
        return '%s' % (self.description)


class Location(models.Model):

    name = models.CharField(max_length=15)
    iso = models.CharField(max_length=15)

    def __str__(self):
        return '%s' % (self.name)


class Category(models.Model):
    name = models.CharField(max_length=15)
    description = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return '%s' % (self.name)


class Subcategory(models.Model):
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=15)
    description = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return '%s' % (self.name)


class Stats(models.Model):
    advertisement = models.ForeignKey(
        'Advertisement',
        on_delete=models.CASCADE,
    )
    searches_appeared_in = models.IntegerField(default=0)
    tags_appeared_in = models.IntegerField(default=0)
    clicks_product_page = models.IntegerField(default=0)
    homepage_appeared_in = models.IntegerField(default=0)

    def __str__(self):
        return '%s' % (self.advertisement)


class WeeklyStats(models.Model):
    advertisement = models.ForeignKey(
        'Advertisement',
        on_delete=models.CASCADE,
    )
    engagement = models.IntegerField(default=0)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return '%s' % (self.advertisement)


class Support(models.Model):
    email = models.CharField(max_length=15)
    query = models.CharField(max_length=500)

    def __str__(self):
        return '%s' % (self.query)
