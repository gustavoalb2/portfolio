from django.contrib import admin
from django.utils.html import format_html

from .models import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Admin para Tecnologias."""

    list_display = ('icone_preview', 'nome', 'order')
    list_display_links = ('nome',)
    list_editable = ('order',)
    search_fields = ('nome',)
    ordering = ('order',)
    readonly_fields = ('icone_preview_grande',)

    fieldsets = (
        (None, {
            'fields': ('nome', 'icone', 'icone_preview_grande', 'order'),
        }),
    )

    def icone_preview(self, obj):
        if obj.icone:
            return format_html(
                '<img src="{}" style="max-height: 32px;" />',
                obj.icone.url,
            )
        return '—'

    icone_preview.short_description = 'Ícone'

    def icone_preview_grande(self, obj):
        if obj.icone:
            return format_html(
                '<img src="{}" style="max-height: 100px;" />',
                obj.icone.url,
            )
        return '(Nenhum ícone enviado)'

    icone_preview_grande.short_description = 'Pré-visualização'
