from django.views.generic import TemplateView
from .models import TeamMember, Rank, CEO


class IndexView(TemplateView):
    template_name = 'team/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.all()
        context['ceo'] = CEO.objects.first()
        return context