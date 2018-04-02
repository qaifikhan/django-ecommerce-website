from django.db import models
from django.template.defaultfilters import slugify
import re, json
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

# Create your models here.

class ProductCategory(models.Model):
	category_name = models.CharField(max_length = 100)
	slug = models.SlugField(max_length = 100, help_text = 'Please enter "-" \n Note: Slug is gonna be Category Name separated by "-"')
	category_image = models.ImageField(upload_to = 'media/images/category/', blank = True)

	def __str__(self):
		return self.category_name

	def save(self, *args, **kargs):
		self.slug = slugify(self.category_name)
		super().save(*args, **kargs)

class PackageType(models.Model):
	package_type = models.CharField(max_length = 20)

	def __str__(self):
		return self.package_type


class Product(models.Model):
	product_name = models.CharField(max_length = 200)
	category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
	slug = models.SlugField(max_length=200, help_text = 'Please enter "-" \n Note: Slug is gonna be Product Name separated by "-"')
	product_image = models.ImageField(upload_to = 'images/product/', blank = True)
	product_description = models.TextField(blank = False)
	mrp = models.DecimalField(max_digits = 8, decimal_places = 2, blank = False, validators = [MinValueValidator(0.1)])
	saleprice = models.DecimalField(max_digits = 8, decimal_places = 2, blank = False, validators = [MinValueValidator(0.1)])
	package_type = models.ForeignKey(PackageType, on_delete = models.CASCADE, blank = False)
	package_qty = models.DecimalField(max_digits = 6, decimal_places = 2, blank = False, validators = [MinValueValidator(1)])
	stock = models.IntegerField(blank = False)

	def __str__(self):
		return self.product_name

	def save(self, *args, **kargs):
		self.slug = slugify(self.product_name)
		super().save(*args, **kargs)

	def to_json(self):
		return json.dumps(self, sort_keys = True, indent = 4)


class Cart(models.Model):
	product = models.ForeignKey(Product, on_delete = models.CASCADE)
	ordered_quantity = models.IntegerField(blank = False, null = False)
	mrp = models.DecimalField(max_digits = 8, decimal_places = 2, blank = False, validators = [MinValueValidator(0.1)])
	saleprice = models.DecimalField(max_digits = 8, decimal_places = 2, blank = False, validators = [MinValueValidator(0.1)])
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	def __str__(self):
		return str(self.product)

	def amount(self):
		return self.ordered_quantity * self.saleprice