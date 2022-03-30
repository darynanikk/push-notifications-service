from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static, settings
from django.views.generic import TemplateView

urlpatterns = [
  path('', include('notifications.urls')),
  path('webpush/', include('webpush.urls')),
  path('admin/', admin.site.urls),
  path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

