from django.contrib import admin
from .models import ProductCategory, Product, PackageType, Cart

# Register your models here.
admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(PackageType)
admin.site.register(Cart)