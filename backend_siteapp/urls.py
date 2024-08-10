from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('category/<int:category_id>/', views.category, name='category'),
    path('blog/', views.blog, name='blog'),
    path('article/<int:article_id>/', views.article, name='article'),
    path('equaliz', views.equalization, name='equaliz'),
    path('favorite', views.favorite, name='favorite'),
    path('subcategory/<int:nish_id>/', views.subcategory, name='subcategory'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('toggle_favorite/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('clear_favorites/', views.clear_favorites, name='clear_favorites'),
    path('toggle_equaliz/<int:product_id>/', views.toggle_equaliz, name='toggle_equaliz')
    ]