from django.views.generic import TemplateView

from core.models import SiteConfig
from experiences.models import WorkExperience
from projects.models import Project
from skills.models import Skill


class LandingPageView(TemplateView):
    """View pública da landing page. Puxa todos os dados do banco."""

    template_name = 'landing/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Configuração do site (singleton)
        context['config'] = SiteConfig.objects.first()

        # Experiências ativas, ordenadas
        context['experiences'] = WorkExperience.objects.filter(ativo=True)

        # Tecnologias ordenadas
        context['skills'] = Skill.objects.all()

        # Projetos ativos, ordenados, com imagens pré-carregadas
        context['projects'] = Project.objects.filter(
            ativo=True
        ).prefetch_related('imagens')

        return context
