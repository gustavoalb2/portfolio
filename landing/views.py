from django.views.generic import TemplateView
from django.db.utils import OperationalError

from core.models import SiteConfig
from experiences.models import WorkExperience
from projects.models import Project
from skills.models import Skill


class LandingPageView(TemplateView):
    """View pública da landing page. Puxa todos os dados do banco."""

    template_name = 'landing/index.html'

    def _safe_first(self, queryset):
        try:
            return queryset.first()
        except OperationalError:
            return None

    def _safe_list(self, queryset):
        try:
            return list(queryset)
        except OperationalError:
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Configuração do site (singleton)
        context['config'] = self._safe_first(SiteConfig.objects.all())

        # Experiências ativas, ordenadas
        context['experiences'] = self._safe_list(
            WorkExperience.objects.filter(ativo=True)
        )

        # Tecnologias ordenadas
        context['skills'] = self._safe_list(Skill.objects.all())

        # Projetos ativos, ordenados, com imagens pré-carregadas
        context['projects'] = self._safe_list(
            Project.objects.filter(ativo=True).prefetch_related('imagens')
        )

        return context
