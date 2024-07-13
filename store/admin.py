from django.contrib import admin
from .models import product,Variation

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')  # Corrected field name
    prepopulated_fields = {'slug': ('product_name',)}

class VariationAdmin(admin.ModelAdmin):
     list_display = ('product', 'variation_category', 'variation_value','is_active')
     list_editable=("is_active",)
     list_filter=('variation_category', 'variation_value','is_active')

# Register your models here.
admin.site.register(product, ProductAdmin)  # Correct model name and admin class
admin.site.register(Variation,VariationAdmin)