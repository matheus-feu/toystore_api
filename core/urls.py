from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('toy_store/', include('toy_store.urls', namespace='toy_store')),
    path('account/', include('account.urls', namespace='account')),
    path('', lambda request: redirect('account:login', permanent=False)),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('api/v1/', include('core.api_urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
