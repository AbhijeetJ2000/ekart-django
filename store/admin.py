from django.contrib import admin
from .models import Category, Product, Variation

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug')
    prepopulated_fields = {'slug': ('category_name',)}

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}

admin.site.register(Product, ProductAdmin)

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_filter = ('product', 'variation_category', 'variation_value')
    
admin.site.register(Variation, VariationAdmin)



