from django.urls import path
from .views import usergame_list
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('reports/usergames', usergame_list)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
