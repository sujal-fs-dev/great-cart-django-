from django.contrib import admin
from .models import product  # Correct model import and capitalization

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')  # Corrected field name
    prepopulated_fields = {'slug': ('product_name',)}

# Register your models here.
admin.site.register(product, ProductAdmin)  # Correct model name and admin class
