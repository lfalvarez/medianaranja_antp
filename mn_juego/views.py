from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from mn_juego.models import Comuna, Distrito


class IndexView(ListView):
    model = Comuna
    template_name = 'index.html'

class DistritoView(DetailView):
    model = Distrito
    template_name = 'resultado.html'

    def get_object(self, queryset=None):
        comuna_being_asked = Comuna.objects.get(slug=self.kwargs['slug'])
        return comuna_being_asked.distrito