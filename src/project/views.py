from django.views.generic import TemplateView, DetailView

from src.project.models import Project


class IndexView(TemplateView):
    template_name = 'project/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        return context

class ProjectDetailView(DetailView):
    template_name = 'project/project_detail.html'
    model = Project