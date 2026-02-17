from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),
    path('', include('frontend.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
