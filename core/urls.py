from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('customer/', include('customer.urls')),
    path('account/', include('account.urls')),
    path('authentication/', include('authentication.urls')),
    path("web/", include("web.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    
   
]

admin.site.index_title = "Shop Management"
admin.site.site_header = "Shop Management Admin"
admin.site.site_title = "Nina Sky Innovation"