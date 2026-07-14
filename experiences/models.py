from django.db import models

from core.models import compress_image


class WorkExperience(models.Model):
    """Experiência profissional exibida na landing page."""

    titulo = models.CharField(
        max_length=200,
        verbose_name='Título',
        help_text='Nome do projeto ou posição (ex: "App Mobile para E-commerce")',
    )
    empresa = models.CharField(
        max_length=200,
        verbose_name='Empresa',
        help_text='Nome da empresa ou cliente',
    )
    descricao = models.TextField(
        verbose_name='Descrição',
        help_text='Descrição curta do trabalho realizado (2-3 linhas)',
    )
    icone = models.ImageField(
        upload_to='experiences/',
        verbose_name='Ícone / Imagem',
        help_text='Imagem ou ícone do card. Tamanho recomendado: 400x300px',
        blank=True,
    )
    link = models.URLField(
        verbose_name='Link "Saiba Mais"',
        blank=True,
        help_text='URL para mais detalhes (opcional)',
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Ordem',
        help_text='Menor número aparece primeiro',
    )
    ativo = models.BooleanField(
        default=True,
        verbose_name='Ativo',
        help_text='Desmarque para ocultar do site sem deletar',
    )

    class Meta:
        ordering = ['order']
        verbose_name = 'Experiência Profissional'
        verbose_name_plural = 'Experiências Profissionais'

    def __str__(self):
        return f'{self.titulo} — {self.empresa}'

    def save(self, *args, **kwargs):
        if self.icone:
            compress_image(self.icone, max_size=(400, 300))
        super().save(*args, **kwargs)
