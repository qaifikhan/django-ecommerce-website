from betterhealth import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^betterhealth/(?P<product_url>[\w\-]+)/$', views.product_detail, name='product detail'),
    url(r'^(?P<category_url>[\w\-]+)/$', views.all_category_products, name='category_products'),
    url(r'^search$', views.search, name = 'search'),
    url(r'^cart/add$', views.add_to_cart, name = 'addtocart'),
    url(r'^cart$', views.get_cart, name = 'viewcart'),
    url(r'^login#', views.login, name = 'login'),
    url(r'^logout#', views.logout, name = 'logout'),
    url(r'^signup#', views.signup, name = 'signup'),
]
