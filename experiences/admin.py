from django.contrib import admin
from django.utils.html import format_html

from .models import WorkExperience


@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    """Admin para Experiências Profissionais."""

    list_display = ('icone_preview', 'titulo', 'empresa', 'order', 'ativo')
    list_display_links = ('titulo',)
    list_editable = ('order', 'ativo')
    list_filter = ('ativo', 'empresa')
    search_fields = ('titulo', 'empresa', 'descricao')
    ordering = ('order',)
    readonly_fields = ('icone_preview_grande',)

    fieldsets = (
        (None, {
            'fields': ('titulo', 'empresa', 'descricao', 'link'),
        }),
        ('Imagem', {
            'fields': ('icone', 'icone_preview_grande'),
        }),
        ('Exibição', {
            'fields': ('order', 'ativo'),
        }),
    )

    def icone_preview(self, obj):
        if obj.icone:
            return format_html(
                '<img src="{}" style="max-height: 40px; border-radius: 4px;" />',
                obj.icone.url,
            )
        return '—'

    icone_preview.short_description = 'Ícone'

    def icone_preview_grande(self, obj):
        if obj.icone:
            return format_html(
                '<img src="{}" style="max-height: 200px; border-radius: 8px;" />',
                obj.icone.url,
            )
        return '(Nenhuma imagem enviada)'

    icone_preview_grande.short_description = 'Pré-visualização'
