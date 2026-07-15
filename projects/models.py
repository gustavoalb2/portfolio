from django.db import models

from core.models import compress_image


class Project(models.Model):
    """Projeto em destaque exibido na landing page."""

    label = models.CharField(
        max_length=100,
        verbose_name='Label',
        default='Projeto em Destaque',
        help_text='Rótulo acima do título (ex: "Projeto em Destaque")',
    )
    titulo = models.CharField(
        max_length=200,
        verbose_name='Título do Projeto',
        help_text='Nome do projeto',
    )
    descricao = models.TextField(
        verbose_name='Descrição',
        help_text='Descrição do projeto (3-5 linhas)',
    )
    imagem_principal = models.ImageField(
        upload_to='projects/',
        verbose_name='Imagem Principal',
        help_text='Screenshot principal do projeto. Tamanho recomendado: 1200x800px',
    )
    link_projeto = models.URLField(
        verbose_name='Link do Projeto',
        blank=True,
        help_text='URL do projeto ao vivo (opcional)',
    )
    link_repositorio = models.URLField(
        verbose_name='Link do Repositório',
        blank=True,
        help_text='URL do repositório no GitHub (opcional)',
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
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        # Compressão desativada por enquanto (causa duplicação de pastas)
        # if self.imagem_principal:
        #     compress_image(self.imagem_principal, max_size=(1200, 800))
        super().save(*args, **kwargs)


class ProjectImage(models.Model):
    """Imagem adicional de um projeto (para carrossel)."""

    projeto = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='imagens',
        verbose_name='Projeto',
    )
    imagem = models.ImageField(
        upload_to='projects/gallery/',
        verbose_name='Imagem',
        help_text='Imagem adicional do projeto. Tamanho recomendado: 1200x800px',
    )
    legenda = models.CharField(
        max_length=200,
        verbose_name='Legenda',
        blank=True,
        help_text='Legenda opcional para a imagem',
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Ordem',
        help_text='Ordem no carrossel (menor primeiro)',
    )

    class Meta:
        ordering = ['order']
        verbose_name = 'Imagem do Projeto'
        verbose_name_plural = 'Imagens do Projeto'

    def __str__(self):
        return f'Imagem {self.order} — {self.projeto.titulo}'

    def save(self, *args, **kwargs):
        # Compressão desativada por enquanto (causa duplicação de pastas)
        # if self.imagem:
        #     compress_image(self.imagem, max_size=(1200, 800))
        super().save(*args, **kwargs)
