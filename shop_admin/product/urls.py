from django.urls import path
from . import views

urlpatterns = [
    path('add-product/', views.add_product, name='add_product'),
    path('my-product/', views.my_products, name='my_products'),
    path('edit-product/<int:id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:id>',views.delete_product,name='delete_product'),
    path('product-detail/<int:id>',views.product_detail,name='product_detail'),
    path('add-to-cart/<int:id>',views.add_to_cart,name='add_to_cart'),
    path('update-cart/',views.update_cart_ajax,name='update_cart'),
    path('cart/',views.cart,name='cart')
]

