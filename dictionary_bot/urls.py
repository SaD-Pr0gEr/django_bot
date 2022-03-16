from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('users/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('telegram/', include('telegram.urls')),
    path('translator/', include('translator.urls')),
    path('', include("bot_admin.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
    urlpatterns += static(settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
