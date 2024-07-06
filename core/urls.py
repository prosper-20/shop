from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('customer/', include('customer.urls')),
    path('account/', include('account.urls')),
    path('authentication/', include('authentication.urls')),
    path("web/", include("web.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.index_title = "Shop Management"
admin.site.site_header = "Shop Management Admin"
admin.site.site_title = "Nina Sky Innovation"