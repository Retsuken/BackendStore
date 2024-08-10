# Generated by Django 4.2 on 2024-05-13 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend_siteapp', '0014_alter_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=156, verbose_name='Заголовок текста')),
                ('image', models.ImageField(upload_to='content_category_image', verbose_name='Фотография')),
                ('text', models.TextField(verbose_name='Текст Контента')),
            ],
        ),
        migrations.AlterModelOptions(
            name='categoryse',
            options={'verbose_name': 'Категории', 'verbose_name_plural': 'Категории'},
        ),
    ]
