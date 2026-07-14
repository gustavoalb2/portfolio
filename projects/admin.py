from django.contrib import admin
from django.utils.html import format_html

from .models import Project, ProjectImage


class ProjectImageInline(admin.TabularInline):
    """Inline para adicionar imagens extras ao projeto."""

    model = ProjectImage
    extra = 1
    readonly_fields = ('imagem_preview',)
    fields = ('imagem', 'imagem_preview', 'legenda', 'order')
    ordering = ('order',)

    def imagem_preview(self, obj):
        if obj.imagem:
            return format_html(
                '<img src="{}" style="max-height: 80px; border-radius: 4px;" />',
                obj.imagem.url,
            )
        return '(Salve para ver a pré-visualização)'

    imagem_preview.short_description = 'Pré-visualização'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin para Projetos com inline de imagens."""

    list_display = ('imagem_preview', 'titulo', 'label', 'order', 'ativo')
    list_display_links = ('titulo',)
    list_editable = ('order', 'ativo')
    list_filter = ('ativo', 'label')
    search_fields = ('titulo', 'descricao')
    ordering = ('order',)
    readonly_fields = ('imagem_preview_grande',)
    inlines = [ProjectImageInline]

    fieldsets = (
        (None, {
            'fields': ('label', 'titulo', 'descricao'),
        }),
        ('Imagem Principal', {
            'fields': ('imagem_principal', 'imagem_preview_grande'),
        }),
        ('Links', {
            'fields': ('link_projeto', 'link_repositorio'),
        }),
        ('Exibição', {
            'fields': ('order', 'ativo'),
        }),
    )

    def imagem_preview(self, obj):
        if obj.imagem_principal:
            return format_html(
                '<img src="{}" style="max-height: 40px; border-radius: 4px;" />',
                obj.imagem_principal.url,
            )
        return '—'

    imagem_preview.short_description = 'Imagem'

    def imagem_preview_grande(self, obj):
        if obj.imagem_principal:
            return format_html(
                '<img src="{}" style="max-height: 250px; border-radius: 8px;" />',
                obj.imagem_principal.url,
            )
        return '(Nenhuma imagem enviada)'

    imagem_preview_grande.short_description = 'Pré-visualização'
