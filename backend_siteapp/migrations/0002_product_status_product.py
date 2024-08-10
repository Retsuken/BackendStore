# Generated by Django 4.2 on 2024-05-10 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_siteapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status_product',
            field=models.CharField(choices=[('in_stock', 'В наличии'), ('out_of_stock', 'Нет в наличии'), ('on_order', 'Под заказ')], default=1, max_length=56),
            preserve_default=False,
        ),
    ]
