# Generated by Django 4.2 on 2024-05-17 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_siteapp', '0019_xar_product_xar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='xar',
            options={'verbose_name': 'О товаре', 'verbose_name_plural': 'О товаре'},
        ),
        migrations.AddField(
            model_name='product',
            name='sposob_paym',
            field=models.CharField(default=1, max_length=156, verbose_name='Способ оплаты'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='sposob_sdek',
            field=models.CharField(default=1, max_length=156, verbose_name='Способ доставки'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='xar',
            field=models.ManyToManyField(to='backend_siteapp.xar', verbose_name='О товаре'),
        ),
    ]
