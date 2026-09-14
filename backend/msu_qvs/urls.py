from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .health import live, ready

urlpatterns = [
    path('health/live/', live, name='health_live'),
    path('health/ready/', ready, name='health_ready'),
    path('admin/', admin.site.urls),
    
    # UI Web Navigation
    path('', include('verification.urls')),
    path('auth/', include('authentication.urls')),
    path('students/', include('students.urls')),
    path('qualifications/', include('qualifications.urls')),
    path('employers/', include('employers.urls')),
    path('reports/', include('reports.urls')),
    path('fraud/', include('ai_fraud.urls')),
    
    # REST API Routes
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
