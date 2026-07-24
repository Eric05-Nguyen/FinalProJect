from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    
    path('product/', include('product.urls')),
    
    path('users/', include('users.urls')),
    path('account/', include('users.account_urls')),
    
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
