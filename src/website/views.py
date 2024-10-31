from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from src.service.models import Service
from .models import Testimonials
from src.team.models import TeamMember
from .forms import ContactForm


# Create your views here.
class IndexView(TemplateView):
    template_name = 'website/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.all()
        context['team_members'] = TeamMember.objects.all()
        context['testimonials'] = Testimonials.objects.all()
        context['contact_form'] = ContactForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('website:index'))

        context = self.get_context_data()
        context['contact_form'] = form
        return self.render_to_response(context)
class ContactView(TemplateView):
    template_name = 'website/contact-us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_form'] = ContactForm()
        return context

class AboutView(TemplateView):
    template_name = 'website/about-us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.all()
        context['testimonials'] = Testimonials.objects.all()

        return context
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('website:index'))

        context = self.get_context_data()
        context['contact_form'] = form
        return self.render_to_response(context)

