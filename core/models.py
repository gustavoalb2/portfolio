import os
from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from PIL import Image


def compress_image(image_field, max_size=(800, 800), quality=85):
    """Redimensiona e comprime uma imagem se for maior que max_size."""
    if not image_field:
        return

    try:
        img = Image.open(image_field)
    except Exception:
        return

    # Converter RGBA para RGB se necessário (para salvar como JPEG)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    # Redimensionar se maior que max_size
    if img.width > max_size[0] or img.height > max_size[1]:
        img.thumbnail(max_size, Image.LANCZOS)

    # Salvar em buffer
    buffer = BytesIO()
    img_format = 'JPEG'
    ext = os.path.splitext(image_field.name)[1].lower()
    if ext == '.png':
        img_format = 'PNG'
    elif ext == '.webp':
        img_format = 'WEBP'

    img.save(buffer, format=img_format, quality=quality, optimize=True)
    buffer.seek(0)

    # Substituir o conteúdo do campo
    image_field.save(
        image_field.name,
        ContentFile(buffer.read()),
        save=False,
    )


class SiteConfig(models.Model):
    """
    Configuração geral do site (singleton).
    Apenas um registro deve existir no banco.
    """

    nome_site = models.CharField(
        max_length=100,
        verbose_name='Nome do Site',
        help_text='Nome exibido no logo da página (ex: "Meu Portfólio")',
    )
    titulo = models.CharField(
        max_length=200,
        verbose_name='Título da Página',
        help_text='Título que aparece na aba do navegador (SEO)',
    )
    headline = models.CharField(
        max_length=300,
        verbose_name='Headline Principal',
        help_text='Frase de impacto no hero (ex: "Judges a book by its cover")',
    )
    subtitulo = models.CharField(
        max_length=300,
        verbose_name='Subtítulo',
        help_text='Texto acima da headline (ex: "Um Desenvolvedor que...")',
    )
    cargo_atual = models.CharField(
        max_length=150,
        verbose_name='Cargo Atual',
        help_text='Seu cargo atual (ex: "Engenheiro de Software")',
    )
    empresa_atual = models.CharField(
        max_length=150,
        verbose_name='Empresa Atual',
        help_text='Nome da empresa onde trabalha atualmente',
    )
    link_empresa = models.URLField(
        verbose_name='Link da Empresa',
        blank=True,
        help_text='URL do site da empresa',
    )
    sobre_mim = models.TextField(
        verbose_name='Sobre Mim',
        help_text='Texto descritivo exibido na seção hero (2-3 frases)',
    )
    foto_perfil = models.ImageField(
        upload_to='profile/',
        verbose_name='Foto de Perfil',
        help_text='Foto/avatar exibido no hero. Tamanho recomendado: 500x500px',
    )
    texto_disponibilidade = models.TextField(
        verbose_name='Texto de Disponibilidade',
        help_text='Texto exibido na seção de tecnologias (ex: "Atualmente buscando ingressar em um time multidisciplinar...")',
    )
    email_contato = models.EmailField(
        verbose_name='E-mail de Contato',
        help_text='E-mail exibido na seção de contato',
    )
    link_github = models.URLField(
        verbose_name='GitHub',
        blank=True,
        help_text='URL do perfil no GitHub',
    )
    link_linkedin = models.URLField(
        verbose_name='LinkedIn',
        blank=True,
        help_text='URL do perfil no LinkedIn',
    )
    link_instagram = models.URLField(
        verbose_name='Instagram',
        blank=True,
        help_text='URL do perfil no Instagram',
    )
    link_twitter = models.URLField(
        verbose_name='Twitter / X',
        blank=True,
        help_text='URL do perfil no Twitter/X',
    )
    meta_description = models.TextField(
        verbose_name='Meta Description (SEO)',
        blank=True,
        help_text='Descrição do site para mecanismos de busca (150-160 caracteres recomendados)',
    )

    class Meta:
        verbose_name = 'Configuração do Site'
        verbose_name_plural = 'Configuração do Site'

    def __str__(self):
        return self.nome_site or 'Configuração do Site'

    def save(self, *args, **kwargs):
        """Garante singleton: só permite 1 registro."""
        self.pk = 1
        # Compressão desativada por enquanto (causa duplicação de pastas)
        # if self.foto_perfil:
        #     compress_image(self.foto_perfil, max_size=(500, 500))
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Carrega a instância singleton ou retorna None."""
        obj, _ = cls.objects.get_or_create(pk=1, defaults={
            'nome_site': 'Meu Portfólio',
            'titulo': 'Portfólio',
            'headline': 'Judges a book by its cover',
            'subtitulo': 'Um Desenvolvedor que...',
            'cargo_atual': 'Desenvolvedor',
            'empresa_atual': 'Empresa',
            'sobre_mim': 'Sobre mim...',
            'texto_disponibilidade': 'Disponível para novos projetos.',
            'email_contato': 'contato@email.com',
        })
        return obj
