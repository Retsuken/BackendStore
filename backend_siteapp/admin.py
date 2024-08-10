from django.contrib import admin
from .models import Product, CategoryArticle, Article, City, ContentHome, Review, ReviewStatus, Nishe, Categoryse, PodCategoryss, ContentCategory, ContentSub, Xar, SmartCharacteristic, Magazin, FilterProduct
from django.contrib import admin
from django.utils.safestring import mark_safe


admin.site.register(Product)
admin.site.register(PodCategoryss)
admin.site.register(Nishe)
admin.site.register(Categoryse)
admin.site.register(CategoryArticle)
admin.site.register(Article)
admin.site.register(City)
admin.site.register(ContentHome)
admin.site.register(ContentCategory)
admin.site.register(ContentSub)
admin.site.register(Xar)
admin.site.register(SmartCharacteristic)
admin.site.register(Magazin)
admin.site.register(FilterProduct)





@admin.action(description='Удовлетворить отзыв')
def approve_reviews(modeladmin, request, queryset):
    ReviewStatus.objects.filter(review__in=queryset).update(status=ReviewStatus.APPROVED)

@admin.action(description='Не удовлетворить отзыв')
def reject_reviews(modeladmin, request, queryset):
    rejected_reviews = queryset.filter(status__status=ReviewStatus.PENDING)
    rejected_reviews.delete()

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'rating', 'status_display')
    actions = [approve_reviews, reject_reviews]

    def status_display(self, obj):
        if obj.status:
            return obj.status.get_status_display()
        else:
            return '-'

    status_display.short_description = 'Status'