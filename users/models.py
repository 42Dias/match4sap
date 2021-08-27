import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls.base import reverse

from localflavor.br.br_states import STATE_CHOICES

class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    email = models.EmailField(unique=True)
    is_headhunter = models.BooleanField(default=False)
    phone = models.CharField(max_length=16, unique=True, blank=True, null=True)
    state = models.CharField(max_length=100, choices=STATE_CHOICES, blank=True, null=True)
    # termos =  models.BooleanField(default=False)

    def get_absolute_url(self):
        if not self.is_headhunter:
            return reverse('pre_professional_profile', args=[str(self.pk)])
        else:
            return reverse('headhunter_profile', args=[str(self.pk)])

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        full_name = f'{self.first_name} {self.last_name}'
        if len(full_name) <= 35:
            return full_name
        elif len(full_name) > 35:
            return f'{full_name[35]}...'