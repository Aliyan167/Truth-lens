from django.views.generic import TemplateView, DetailView
from .models import Service
from src.website.models import Testimonials

class IndexView(TemplateView):
    template_name = 'service/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        context['testimonials'] = Testimonials.objects.all()
        return context

class ServiceDetailView(DetailView):
    template_name = 'service/service_detail.html'
    model = Service

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()[:6]
        return context