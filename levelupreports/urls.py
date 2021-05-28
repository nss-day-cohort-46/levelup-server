from django.urls import path
from .views import usergame_list, events_by_user
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('reports/usergames', usergame_list),
    path('reports/userevents', events_by_user)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
