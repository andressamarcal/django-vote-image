from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Template(models.Model):

    VOTE_CHOICES = (
        (-1, 'Negativo'),
        (0, 'Neutro'),
        (1, 'Positivo'),
    )

    vote = models.SmallIntegerField(choices=VOTE_CHOICES, verbose_name='Voto')
    img_user = models.ForeignKey(
        User, on_delete=models.PROTECT, blank=True, verbose_name='Quem gabaritou')
    filename = models.CharField(max_length=50, verbose_name='Nome do Arquivo')
    created_at = models.DateTimeField(
        default=datetime.now, blank=True, verbose_name='Data e Hora')

    def __str__(self):
        return self.filename

    class Meta:
        verbose_name_plural = "Images"
        ordering = ['filename']