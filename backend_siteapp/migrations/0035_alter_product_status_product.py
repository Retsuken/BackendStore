# Generated by Django 4.2 on 2024-06-03 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_siteapp', '0034_alter_product_status_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='status_product',
            field=models.CharField(choices=[('В наличии', 'В наличии'), ('Нет в наличии', 'Нет в наличии'), ('Под заказ', 'Под заказ')], max_length=56),
        ),
    ]
