from django.urls import path

from mn_juego.views import IndexView, DistritoView


app_name = 'mn_juego'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<slug:slug>', DistritoView.as_view(), name='distrito_detail'),
]