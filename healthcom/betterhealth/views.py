from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from .models import ProductCategory, Product, Cart

# Create your views here.

def index(request):
	categories = ProductCategory.objects.all()
	cart = Cart.objects.filter(user = request.user.pk)
	context_dict = {
		"categories" : categories,
		"cart" : cart
	}
	return render(request, "home.html", context_dict)


def product_detail(request, product_url):
	product = Product.objects.get(slug = product_url)
	cart = Cart.objects.filter(user = request.user.pk)
	context_dict = {
	    "product" : product,
		"cart" : cart
	}
	return render(request, "product_details.html", context_dict)

def search(request):
	if request.method == 'GET':
		search_string = request.GET.get('search')
		cart = Cart.objects.filter(user = request.user.pk)
		search_results = Product.objects.filter(product_name__icontains = search_string)
		context_dict = {
			"search_results":search_results,
			"search_string":search_string,
			"cart":cart
		}
		return render(request, "search_results.html", context_dict)
	else:
		context_dict = {
			"search_results":None,
			"search_string":search_string,
			"cart":cart
		}
		return render(request, "search_results.html", context_dict)


def all_category_products(request, category_url):
	category = ProductCategory.objects.get(slug = category_url)
	cart = Cart.objects.filter(user = request.user.pk)
	context_dict = {
	    "category" : category,
		"cart" : cart
	}
	return render(request, "category_products.html", context_dict)
	

def add_to_cart(request):
	if request.method == 'POST':
		quantity = request.POST.get('quantity')
		product = request.POST.get('product')
		req_product = Product.objects.get(product_name = product)
		print("User PK => ", request.user.pk)
		print("Requested Qty => ", quantity)

		instance = Cart(product = req_product, ordered_quantity = quantity, mrp = req_product.mrp, saleprice = req_product.saleprice, user = request.user)
		instance.save()

		cart = Cart.objects.filter(user = request.user.pk)
		context_dict = {
	    	"product" : req_product,
	    	"cart" : cart
		}
		return render(request, "product_details.html", context_dict)
	else:
		return render(request, "product_details.html", {"product" : None})



def get_cart(request):
	cart = Cart.objects.filter(user = request.user.pk)

	total_amount = 0.0 
	for cart_item in cart:
		total_amount += float(Cart.amount(cart_item))
	context_dict = {
    	"cart" : cart,
    	"total_amount": total_amount
	}
	return render(request, "cart.html", context_dict)



def login(request):
	if request.method == 'POST':
		username = request.POST.get('Username')
		password = request.POST.get('Password')
		user = authenticate(request, username = username, password = password)
		print("Username", username)
		print("Password", password)

		if user is not None:
			auth_login(request, user)
			print("Username ", user.username)
		else:
			print("Login failed")

		categories = ProductCategory.objects.all()
		cart = Cart.objects.filter(user = request.user.pk)
		context_dict = {
			"categories" : categories,
			"cart" : cart
		}
		return render(request, "home.html", context_dict)


def logout(request):
	auth_logout(request)

	categories = ProductCategory.objects.all()
	cart = Cart.objects.filter(user = request.user.pk)
	context_dict = {
		"categories" : categories,
		"cart" : cart
	}
	return render(request, "home.html", context_dict)


def signup(request):
	if request.method == 'POST':
		username = request.POST.get('Username')
		email = request.POST.get('Email')
		password = request.POST.get('Password')

		user = User.objects.create_user(username, email, password)

		if authenticate(request, username = username, password = password):
			categories = ProductCategory.objects.all()
			cart = Cart.objects.filter(user = request.user.pk)
			context_dict = {
				"categories" : categories,
				"cart" : cart
			}
			return render(request, "home.html", context_dict)
		else:
			return HttpResponse("Error:", "Cannot create user")