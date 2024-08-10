from django.db import models
from django.utils.translation import gettext_lazy as _
from filer.fields.image import FilerImageField
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator




    
class Nishe(models.Model):
    name = models.CharField(_("Название низшей подкатегории"), max_length=156)
    value = models.TextField(_("Значение"))
    class Meta:
        verbose_name = 'Низшие подкатегории'
        verbose_name_plural = 'Низшие подкатегории'

    def __str__(self):
        return self.name

class PodCategoryss(models.Model):
    name = models.CharField("Название подкатегории", max_length=156)
    nish_category = models.ManyToManyField(Nishe, verbose_name='Низшие подкатегории')
    image = models.ImageField(_("Фото подкатегории"), null=True, blank=True, upload_to='pod_category_image')
    class Meta:
        verbose_name = 'Подкатегории Категорий'
        verbose_name_plural = 'Подкатегории Категорий'

    def __str__(self):
        return self.name

class Categoryse(models.Model):
    name = models.CharField(_("Название категории"), max_length=156)
    image = models.ImageField(_("Изображение категории"), upload_to='categoryhome_image')
    pod_category = models.ManyToManyField(to=PodCategoryss, verbose_name='Подкатегория Категории')
    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class ContentSub(models.Model):
    name = models.CharField(_("Название контента"), max_length=156)
    image = models.ImageField(_("Фото контента"), upload_to='sub_category_content_image')
    text = models.TextField(_("Текст контента"))


    class Meta:
        verbose_name = 'Контент (subcategory.html)'
        verbose_name_plural = 'Контент (subcategory.html)'

    def __str__(self):
        return self.name


class Xar(models.Model):
    name = models.CharField(_("Название"), max_length=156)
    text = models.CharField(_("Значение"), max_length=156)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'О товаре'
        verbose_name_plural = 'О товаре'
   
class SmartCharacteristic(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', null=True, blank=True)
    value = models.CharField(max_length=100, verbose_name='Значение', null=True, blank=True)
    name_w = models.CharField(max_length=100, verbose_name='Название цвета', null=True, blank=True)
    hex_code = models.CharField(max_length=7, verbose_name='Hex-код цвета', null=True, blank=True)
    def __str__(self):
        return f'{self.name} | {self.value} | {self.name_w} | {self.hex_code}'

    class Meta:
        verbose_name = 'Умная характеристика'
        verbose_name_plural = 'Умные характеристики'

class Magazin(models.Model):
    logo = models.ImageField(upload_to='logo_images', verbose_name='Лого магазина')
    name = models.CharField(_('Название магазина'), max_length=156)
    description = models.TextField(_('Описание магазина'))
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Магазины'
        verbose_name_plural = 'Магазины'

  
class ReviewStatus(models.Model):
    PENDING = 'Не проверен'
    APPROVED = 'Удовлетворён'
    REJECTED = 'Не удовлетворён'
    STATUS_CHOICES = [
        (PENDING, 'Не проверен'),
        (APPROVED, 'Удовлетворён'),
        (REJECTED, 'Не удовлетворён'),
    ]
    status = models.CharField(max_length=56, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return self.get_status_display()


class Review(models.Model):
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[MinValueValidator(0.5), MaxValueValidator(5)],
        verbose_name='Оценка',
        help_text='Оценка от 0,5 до 5 с шагом 0,5',
    )
    dost = models.TextField(_("Достоинства"))
    nedos = models.TextField(_("Недостатки"))
    obj = models.TextField(_("Общие впечатления"))
    image = models.ImageField(_("Фотографии"), upload_to='review_images')
    name = models.CharField(_("Имя"), max_length=156)
    email = models.EmailField(_("Почта"))
    created_at = models.DateField(_("Дата"), default=timezone.now, null=True, blank=True)
    status = models.OneToOneField(ReviewStatus, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Отзывы'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Имя: {self.name} | Оценка: {self.rating}'
    

    def save(self, *args, **kwargs):
        if not self.pk:  # Если это новый объект
            self.status = ReviewStatus.objects.create()
        super().save(*args, **kwargs)



class FilterProduct(models.Model):
    name = models.CharField(_("Название"), max_length=156)
    value = models.CharField(_("Значение"), max_length=156)

    class Meta:
        verbose_name = 'Фильтрация (Товары)'
        verbose_name_plural = 'Фильтрация (Товары)'

    def  __str__(self):
        return f'Название: {self.name} | Значение: {self.value}'  



class Product(models.Model):

    STATUS_CHOICES = [
        ('В наличии', 'В наличии'),
        ('Нет в наличии', 'Нет в наличии'),
        ('Под заказ', 'Под заказ'),
    ]
    name = models.CharField(_("Название товара"), max_length=156)
    images = FilerImageField(null=True, blank=True, on_delete=models.SET_NULL, related_name="product_images")
    price = models.IntegerField(_("Цена"))
    new = models.BooleanField()
    xit = models.BooleanField(_("Хит"))
    category = models.ManyToManyField(Nishe, verbose_name='Категория')
    articles = models.ManyToManyField('backend_siteapp.Article', blank=True, related_name="products_set")
    status_product = models.CharField(max_length=56, choices=STATUS_CHOICES)
    xar = models.ManyToManyField(Xar, verbose_name='О товаре')
    sposob_paym = models.CharField(_("Способ оплаты"), max_length=156)
    sposob_sdek = models.CharField(_("Способ доставки"), max_length=156)
    smart_characteristics = models.ManyToManyField(SmartCharacteristic, verbose_name='Умные характеристики', blank=True)
    magaz = models.ManyToManyField(Magazin, verbose_name='Магазин', blank=True)
    reviews = models.ManyToManyField(Review, related_name='product', blank=True)
    filter = models.ManyToManyField(FilterProduct, verbose_name='Фильтрация', blank=True)
    pod_category = models.ForeignKey(PodCategoryss, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Товары'
        verbose_name_plural = 'Товары'



class ProductView(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='views')
    viewed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"View on {self.product.name} at {self.viewed_at}"





class CategoryArticle(models.Model):
    category = models.CharField(_("Категория статьи"), max_length=156)


    class Meta:
        verbose_name = 'Категории (статьи)'
        verbose_name_plural = 'Категории (статьи)'


    def __str__(self):
        return self.category
    

class ContentCategory(models.Model):
    name = models.CharField(_("Заголовок текста"), max_length=156)
    image = models.ImageField(_("Фотография"), upload_to='content_category_image')
    text = models.TextField(_("Текст Контента"))
    

    class Meta:
        verbose_name = 'Контент (category.html)'
        verbose_name_plural = 'Контент (category.html)'


    def __str__(self):
        return self.name



class Article(models.Model):
    zagolovok = models.CharField(_("Заголовок статьи"), max_length=156)
    text = models.TextField(_("Текст статьи"))
    pod_zagolovok = models.CharField(_("Подзаголовок статьи"), max_length=156)
    image = models.ImageField(_("Фото статьи"), upload_to='article_image')
    category = models.ForeignKey(to=CategoryArticle, on_delete=models.CASCADE, verbose_name='Категория')
    tovar = models.ForeignKey('backend_siteapp.Product', on_delete=models.CASCADE, verbose_name="Товар", null=True, blank=True, related_name="articles_set", related_query_name="article")
    created_at = models.DateTimeField(_("Дата создания"), default=timezone.now)
    view_count = models.PositiveIntegerField(default=0, verbose_name='Количество переходов')
    class Meta:
        verbose_name = 'Статьи'
        verbose_name_plural = 'Статьи'


    def __str__(self):
        return self.zagolovok




class City(models.Model):
    city = models.CharField(_("Город/Регион"), max_length=156)
    
    class Meta:
        verbose_name = 'Города/Регионы'
        verbose_name_plural = 'Города/Регионы'


    def __str__(self):
        return self.city
    

class ContentHome(models.Model):
    zagolovok = models.CharField(_("Заголовок контента"), max_length=156)
    text = models.TextField(_("Текст контента"))
    image = models.ImageField(_("Фото контента"), upload_to='contenthome_images')

    class Meta:
        verbose_name = 'Контент (Домашняя страница)'
        verbose_name_plural = 'Контент (Домашняя страница)'


    def __str__(self):
        return self.zagolovok
    



