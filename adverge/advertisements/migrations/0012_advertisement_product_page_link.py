# Generated by Django 2.2.3 on 2019-08-26 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0011_stats_homepage_appeared_in'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='product_page_link',
            field=models.CharField(default='amazon.in', max_length=50),
            preserve_default=False,
        ),
    ]
