from django.urls import path

from mn_juego.views import (IndexView,
                            DistritoView,
                            DistritoBySlug,
                            ComunaView,
                            PuebloOriginarioDetailView)


app_name = 'mn_juego'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('c/<slug:slug>', DistritoView.as_view(), name='distrito_detail'),
    path('<slug:slug>', DistritoBySlug.as_view(), name='distrito_detail_by_distrito_slug'),
    path('comuna/<slug:slug>', ComunaView.as_view(), name='comuna_detail'),
    path('pueblos_originarios/<slug:slug>', PuebloOriginarioDetailView.as_view(), name='pueblo_originario_detail'),
]