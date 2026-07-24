from django.urls import path
from . import views
from product import views as product_views 
urlpatterns = [
   path('update/', views.account_update, name='account_update'),
   path('add-product/', product_views.add_product, name='add_product'),
   path('my-product/', product_views.my_products, name='my_products'),
   path('edit-product/<int:id>/', product_views.edit_product, name='edit_product'),
]