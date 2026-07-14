from django.db import models

from core.models import compress_image


class Skill(models.Model):
    """Tecnologia/habilidade exibida na seção orbital."""

    nome = models.CharField(
        max_length=100,
        verbose_name='Nome da Tecnologia',
        help_text='Ex: "Python", "React", "Docker"',
    )
    icone = models.ImageField(
        upload_to='skills/',
        verbose_name='Ícone',
        help_text='Ícone da tecnologia (PNG com fundo transparente). Tamanho recomendado: 80x80px',
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Ordem',
        help_text='Menor número aparece primeiro na órbita',
    )

    class Meta:
        ordering = ['order']
        verbose_name = 'Tecnologia'
        verbose_name_plural = 'Tecnologias'

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if self.icone:
            compress_image(self.icone, max_size=(200, 200))
        super().save(*args, **kwargs)
