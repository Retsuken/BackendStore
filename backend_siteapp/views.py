from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Product, CategoryArticle, Article, ProductView, City, ContentHome, Review, ReviewStatus, Categoryse, PodCategoryss, Nishe, ContentCategory, ContentSub
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from collections import Counter
from django.http import HttpRequest
import re
from django.core.paginator import Paginator
from django.db.models import Avg
from django.db.models import Min, Max
from django.views.decorators.cache import cache_page




def clear_favorites(request):
    request.session['favorites'] = []
    return redirect('favorite')

    


def equalization(request):
    query = request.GET.get('q', '')
    cities = City.objects.all()
    if query:
        cities = cities.filter(city__icontains=query)
    category = Categoryse.objects.all()
    pod_cat = PodCategoryss.objects.all()
    nish = Nishe.objects.all()

    equaliz_product_ids = request.session.get('equaliz', [])
    equaliz_products = Product.objects.filter(id__in=equaliz_product_ids)



    equaliz_products_with_stats = {
        p: {
            'average_rating': p.reviews.filter(status__status=ReviewStatus.APPROVED).aggregate(Avg('rating'))['rating__avg'] or None,
            'num_reviews': p.reviews.filter(status__status=ReviewStatus.APPROVED).count(),
        }
        for p in equaliz_products
    }



    return render(request, 'equalization.html', {'cities': cities,'query': query, 'category': category, 'pod_cat': pod_cat, 'nish': nish, 'equaliz_products': equaliz_products_with_stats,})


 
def toggle_equaliz(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    equaliz = request.session.get('equaliz', [])

    if product.id in equaliz:
        equaliz.remove(product.id)
    else:
        equaliz.append(product.id)

    request.session['equaliz'] = equaliz
    return redirect('equaliz')


def favorite(request):
    query = request.GET.get('q', '')
    statuses = request.GET.getlist('status')  # Получение списка статусов
    cities = City.objects.all()
    favorite_product_ids = request.session.get('favorites', [])
    favorite_products = Product.objects.filter(id__in=favorite_product_ids)

    if statuses:
        favorite_products = favorite_products.filter(status_product__in=statuses) 

    favorite_products_with_stats = {
        p: {
            'average_rating': p.reviews.filter(status__status=ReviewStatus.APPROVED).aggregate(Avg('rating'))['rating__avg'] or None,
            'num_reviews': p.reviews.filter(status__status=ReviewStatus.APPROVED).count(),
        }
        for p in favorite_products
    }

    if query:
        cities = cities.filter(city__icontains=query)

    category = Categoryse.objects.all()
    pod_cat = PodCategoryss.objects.all()
    nish = Nishe.objects.all()
    selected_statuses = request.GET.getlist('status')
    context = {
        'cities': cities,
        'query': query,
        'favorite_products': favorite_products_with_stats,
        'category': category, 
        'pod_cat': pod_cat, 
        'nish': nish,
        'product_statuses': Product.objects.values_list('status_product', flat=True).distinct(),
        'selected_statuses': selected_statuses,
    }


    return render(request, 'favorite.html', context)

def subcategory(request, nish_id):
    query = request.GET.get('q', '')
    cities = City.objects.all()
    if query:
        cities = cities.filter(city__icontains=query)
    category = Categoryse.objects.all()
    pod_cat = PodCategoryss.objects.all()
    nish = Nishe.objects.all()
    content = ContentSub.objects.all()
    # Фильтрация товаров по выбранной категории
    selected_category = Nishe.objects.get(id=nish_id)
    products = Product.objects.filter(category=selected_category)

    products_with_stats = {
        p: {
            'average_rating': p.reviews.filter(status__status=ReviewStatus.APPROVED).aggregate(Avg('rating'))['rating__avg'] or None,
            'num_reviews': p.reviews.filter(status__status=ReviewStatus.APPROVED).count(),
        }
        for p in Product.objects.filter(category=selected_category)
    }


    return render(request, 'subcategory.html', {'cities': cities, 'query': query, 'category': category, 'pod_cat': pod_cat, 'nish': nish, 'products': products_with_stats, 'content': content})


def home(request):
    query = request.GET.get('q', '')
    cities = City.objects.all()
    content = ContentHome.objects.all()
    articles = Article.objects.all().order_by('-created_at')
    if query:
        cities = cities.filter(city__icontains=query)
    category = Categoryse.objects.all()
    pod_cat = PodCategoryss.objects.all()
    nish = Nishe.objects.all()
    popular_products = Product.objects.annotate(view_count=Count('views')).order_by('-view_count')[:5]
    viewed_product_ids = request.session.get('viewed_products', [])
    viewed_products = Product.objects.filter(id__in=viewed_product_ids)


    viewed_products_with_stats = {
        p: {
            'average_rating': p.reviews.filter(status__status=ReviewStatus.APPROVED).aggregate(Avg('rating'))['rating__avg'] or None,
            'num_reviews': p.reviews.filter(status__status=ReviewStatus.APPROVED).count(),
        }
        for p in Product.objects.filter(id__in=viewed_product_ids)
    }

    popular_products_with_stats = []
    for p in popular_products:
        reviews = p.reviews.filter(status__status=ReviewStatus.APPROVED)
        if reviews:
            average_rating_for_product = reviews.aggregate(Avg('rating'))['rating__avg']
            num_reviews_for_product = reviews.count()
        else:
            average_rating_for_product = None
            num_reviews_for_product = 0
        popular_products_with_stats.append((p, average_rating_for_product, num_reviews_for_product, p.view_count))





    context = {
        'popular_products': popular_products_with_stats,
        'viewed_products': viewed_products_with_stats,
        'cities': cities,
        'query': query,
        'content': content,
        'articles': articles,
        'category': category,
        'pod_cat': pod_cat,
        'nish': nish
    }

    return render(request, 'index.html', context)



 
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorites = request.session.get('favorites', [])

    if product.id in favorites:
        favorites.remove(product.id)
    else:
        favorites.append(product.id)

    request.session['favorites'] = favorites
    return redirect('favorite')

def product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    characteristic_values = Nishe.objects.filter(product=product)
    same_category_products = Product.objects.filter(category__in=product.category.all()).exclude(pk=product.pk)
    cities = City.objects.all()
    query = request.GET.get('q', '')
    category = Categoryse.objects.all()
    pod_cat = PodCategoryss.objects.all()
    nish = Nishe.objects.all()
    if query:
        cities = cities.filter(city__icontains=query)



    # Получаем список просмотренных товаров из сессии
    viewed_products = request.session.get('viewed_products', [])

    # Добавляем текущий просмотренный товар в начало списка
    if product_id not in viewed_products:
        viewed_products.insert(0, product_id)
        # Ограничиваем список до 10 последних просмотренных товаров
        viewed_products = viewed_products[:10]
        request.session['viewed_products'] = viewed_products

    # Получаем похожие товары
    similar_products = Product.objects.filter(category__in=product.category.all()).exclude(pk=product.pk) | Product.objects.filter(name=product.name).exclude(pk=product.pk)

    # Получаем связанные статьи для данного продукта
    related_articles = product.articles.all()

    product_smart_characteristics = product.smart_characteristics.all()

    # Получаем продукты с такими же названиями, но с другими значениями умных характеристик
    similar_products_by_smart_characteristics = Product.objects.filter(
        name=product.name
    ).exclude(
        pk=product.pk
    ).prefetch_related(
        'smart_characteristics'
    ).distinct()

    satisfied_reviews = product.reviews.filter(status__status=ReviewStatus.APPROVED)

    if satisfied_reviews:
        average_rating = satisfied_reviews.aggregate(Avg('rating'))['rating__avg']
    else:
        average_rating = None
    
    # Вычисляем среднюю оценку для каждого похожего товара

    selected_filters = request.GET.getlist('filter')
    
    if selected_filters:
        same_category_products = same_category_products.filter(filter__in=selected_filters)

    # Вычисляем среднюю оценку для каждого товара
    same_category_products_with_ratings = []
    for p in same_category_products:  # Используем отфильтрованный список, если есть
        reviews = p.reviews.filter(status__status=ReviewStatus.APPROVED)
        if reviews:
            average_rating_for_product = reviews.aggregate(Avg('rating'))['rating__avg']
            num_reviews_for_product = reviews.count()
        else:
            average_rating_for_product = None
            num_reviews_for_product = 0
        same_category_products_with_ratings.append((p, average_rating_for_product, num_reviews_for_product))



    same_category_product_filters = []
    for product in same_category_products:
        same_category_product_filters.extend(product.filter.all())
# Делаем список уникальных фильтров
    same_category_product_filters = list(set(same_category_product_filters))


    same_name_products = Product.objects.filter(name=product.name)
    min_price = same_name_products.aggregate(min_price=Min('price'))['min_price']

# Найти максимальную цену среди всех товаров с одинаковым названием
    max_price = same_name_products.aggregate(max_price=Max('price'))['max_price']



    context = {
        'product': product,
        'product_filters': same_category_product_filters,
        'characteristic_values': characteristic_values,
        'category': product.category,
        'cities': cities,
        'query': query,
        'magazs': product.magaz.all(),
        'similar_products': similar_products,  # Добавляем похожие товары в контекст
        'satisfied_reviews': satisfied_reviews,
        'related_articles': related_articles,
        'category': category,
        'pod_cat': pod_cat,
        'nish': nish,
        'same_category_products': same_category_products_with_ratings,
        'product_smart_characteristics': product_smart_characteristics,
        'similar_products_by_smart_characteristics': similar_products_by_smart_characteristics,
        'average_rating': average_rating,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'product.html', context)


def submit_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        dost = request.POST.get('dost')
        nedos = request.POST.get('nedos')
        obj = request.POST.get('obj')
        image = request.FILES.get('image')
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Обработка рейтинга
        if rating == 'half':
            rating_value = 0.5
        elif rating == '1 and a half':
            rating_value = 1.5
        elif rating == '2 and a half':
            rating_value = 2.5
        elif rating == '3 and a half':
            rating_value = 3.5
        elif rating == '4 and a half':
            rating_value = 4.5
        else:
            rating_value = float(rating)

        # Создание нового экземпляра Review
        review = Review.objects.create(
            rating=rating_value,
            dost=dost,
            nedos=nedos,
            obj=obj,
            image=image,
            name=name,
            email=email
        )

        # Добавление отзыва в связанные отзывы товара
        product.reviews.add(review)
        product.save()

        # Здесь можно добавить дополнительную логику, например, отправить письмо на почту

        # Перенаправление на страницу товара после успешной отправки отзыва
        return redirect('product', product_id=product.id)

    # Если не POST запрос, перенаправить на страницу товара
    return redirect('product', product_id=product.id)




def category(request, category_id):
    query = request.GET.get('q', '')
    cities = City.objects.all()
    if query:
        cities = cities.filter(city__icontains=query)
    category = get_object_or_404(Categoryse, id=category_id)
    pod_cat = category.pod_category.all()
    categoryes = Categoryse.objects.all()
    nish = Nishe.objects.all()
    articles = Article.objects.all().order_by('-created_at')
    content = ContentCategory.objects.all()
    return render(request, 'category.html', {'cities': cities,'query': query, 'category': category, 'pod_cat': pod_cat, 'nish': nish, 'articles': articles, 'content': content, 'categoryes': categoryes})

def blog(request):
    query = request.GET.get('q', '')
    cities = City.objects.all()
    if query:
        cities = cities.filter(city__icontains=query)
    categories = CategoryArticle.objects.all()
    articles = Article.objects.all().order_by('-created_at')


    category_id = request.GET.get('category', None)
    if category_id:
        category = CategoryArticle.objects.get(id=category_id)
        articles = articles.filter(category=category)

    category = Categoryse.objects.all()
    pod_cat = PodCategoryss.objects.all()
    nish = Nishe.objects.all()

    paginator = Paginator(articles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'page_obj': page_obj, # Объект Paginator
        'articles': page_obj.object_list, # Список статей для текущей страницы
        'cities': cities,
        'query': query,
        'category': category,
        'pod_cat': pod_cat,
        'nish': nish
    }

    return render(request, 'blog.html', context)

def article(request, article_id):
    query = request.GET.get('q', '')
    cities = City.objects.all()
    if query:
        cities = cities.filter(city__icontains=query)

    article = get_object_or_404(Article, pk=article_id)
    article.view_count += 1  # увеличиваем счетчик посещений
    article.save()  # сохраняем изменения в базе данных

    popular_articles = Article.objects.annotate(view_count_annotated=Count('view_count')).order_by('-view_count_annotated')[:3]

    product = article.tovar
    characteristic_values = Nishe.objects.filter(product=product)

    popular_products = Product.objects.annotate(view_count=Count('views')).order_by('-view_count')[:5]


    popular_products_with_stats = []
    for p in popular_products:
        reviews = p.reviews.filter(status__status=ReviewStatus.APPROVED)
        if reviews:
            average_rating_for_product = reviews.aggregate(Avg('rating'))['rating__avg']
            num_reviews_for_product = reviews.count()
        else:
            average_rating_for_product = None
            num_reviews_for_product = 0
        popular_products_with_stats.append((p, average_rating_for_product, num_reviews_for_product, p.view_count))


    category = Categoryse.objects.all()
    pod_cat = PodCategoryss.objects.all()
    nish = Nishe.objects.all()



    satisfied_reviews = product.reviews.filter(status__status=ReviewStatus.APPROVED)

    if satisfied_reviews:
        average_rating = satisfied_reviews.aggregate(Avg('rating'))['rating__avg']
    else:
        average_rating = None


    context = {
        'article': article,
        'category': article.category,
        'product': product,
        'characteristic_values': characteristic_values,
        'popular_products': popular_products_with_stats,
        'cities': cities,
        'query': query,
        'popular_articles': popular_articles,
        'category': category,
        'pod_cat': pod_cat,
        'nish': nish,
        'satisfied_reviews': satisfied_reviews,
        'average_rating': average_rating,
    }

    return render(request, 'article.html', context)