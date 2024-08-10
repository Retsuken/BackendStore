# Generated by Django 4.2 on 2024-05-18 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_siteapp', '0021_smartcharacteristic_product_smart_characteristics'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smartcharacteristic',
            name='description',
        ),
        migrations.AddField(
            model_name='smartcharacteristic',
            name='value',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Значение'),
        ),
    ]
