from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    path('webpush/', include('webpush.urls')),
    path('', include('app_accounts.urls')),
    path('super_admin/', include('app_admin.urls')),
    path('ecc/', include('app_ecc.urls')),
    path('customer/', include('app_customer.urls')),
    path('products/', include('app_products.urls')),

    path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
urlpatterns = urlpatterns+static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)
handler404 = "main_aas.views.notfound404"
handler500 = "main_aas.views.notfound500"
