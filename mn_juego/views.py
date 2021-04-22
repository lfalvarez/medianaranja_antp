from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView, TemplateView
from mn_juego.models import Comuna, Distrito, PuebloOriginario
from django.urls import reverse_lazy


class IndexView(ListView):
    model = Comuna
    template_name = 'index.html'


class DistritoView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        comuna_being_asked = Comuna.objects.get(slug=self.kwargs['slug'])
        distrito_slug = comuna_being_asked.distrito.slug
        return reverse_lazy('mn_juego:distrito_detail_by_distrito_slug',
                            kwargs={'slug': distrito_slug}
                            )


class DistritoBySlug(DetailView):
    model = Distrito
    template_name = 'resultado.html'


class ComunaView(DetailView):
    model = Distrito
    template_name = 'resultado.html'

    def get_object(self, queryset=None):
        self.comuna_being_asked = Comuna.objects.get(slug=self.kwargs['slug'])
        return self.comuna_being_asked.distrito

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['comuna'] = self.comuna_being_asked
        return context


class PuebloOriginarioDetailView(DetailView):
    model = PuebloOriginario
    template_name = 'resultado_pueblos_originarios.html'


class EmbedSearcherView(TemplateView):
    template_name = "embed.html"

    @method_decorator(xframe_options_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
