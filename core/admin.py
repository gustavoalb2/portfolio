from django.contrib import admin
from django.utils.html import format_html

from .models import SiteConfig


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    """Admin para SiteConfig (singleton)."""

    list_display = ('nome_site', 'cargo_atual', 'empresa_atual', 'email_contato')
    readonly_fields = ('foto_preview',)

    fieldsets = (
        ('Identidade', {
            'fields': ('nome_site', 'titulo', 'meta_description'),
        }),
        ('Hero', {
            'fields': ('foto_perfil', 'foto_preview', 'subtitulo', 'headline', 'sobre_mim'),
        }),
        ('Profissional', {
            'fields': ('cargo_atual', 'empresa_atual', 'link_empresa', 'texto_disponibilidade'),
        }),
        ('Contato e Redes Sociais', {
            'fields': ('email_contato', 'link_github', 'link_linkedin', 'link_instagram', 'link_twitter'),
        }),
    )

    def foto_preview(self, obj):
        """Exibe miniatura da foto de perfil."""
        if obj.foto_perfil:
            return format_html(
                '<img src="{}" style="max-height: 150px; border-radius: 50%;" />',
                obj.foto_perfil.url,
            )
        return '(Nenhuma foto enviada)'

    foto_preview.short_description = 'Pré-visualização da Foto'

    def has_add_permission(self, request):
        """Impede criar mais de uma instância."""
        if SiteConfig.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        """Impede deletar a configuração."""
        return False
