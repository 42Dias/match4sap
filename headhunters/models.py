import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator

from localflavor.br.br_states import STATE_CHOICES

from professionals.choices import MODULES_LIST, METHODOLOGY_LIST, INDUSTRIES_LIST

class Job(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    state = models.CharField(max_length=100, choices=STATE_CHOICES, blank=True, null=True)
    working_years = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(38)])
    implementations = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(38)])
    supports = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MaxValueValidator(38)])
    modules = models.CharField(
        max_length=200,
        choices=MODULES_LIST,
        null=True,
        blank=True,
    )
    industries = models.CharField(
        max_length=120,
        choices=INDUSTRIES_LIST,
        null=True,
        blank=True,
    )
    methodology = models.CharField(
        max_length=70,
        choices=METHODOLOGY_LIST,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ('special_status', 'Can access headhunter data'),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('connection', args=[str(self.id)])


class Headhunter(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        primary_key=True,
        editable=False
        )
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True)
    cnpj = models.CharField(max_length=18, unique=True, blank=True, null=True)
    tokens = models.IntegerField(default=2, editable=False)
    tokens_total = models.IntegerField(default=2, editable=False)
    address = models.CharField(max_length=255, blank=True, null=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.email