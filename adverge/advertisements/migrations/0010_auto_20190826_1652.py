# Generated by Django 2.2.3 on 2019-08-26 16:52

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0009_auto_20190721_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='locations',
            field=models.ManyToManyField(blank=True, to='advertisements.Location'),
        ),
        migrations.CreateModel(
            name='WeeklyStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('engagement', models.IntegerField(default=0)),
                ('date', models.DateField(default=datetime.date.today)),
                ('advertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisements.Advertisement')),
            ],
        ),
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('searches_appeared_in', models.IntegerField(default=0)),
                ('tags_appeared_in', models.IntegerField(default=0)),
                ('clicks_product_page', models.IntegerField(default=0)),
                ('advertisement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisements.Advertisement')),
            ],
        ),
    ]
