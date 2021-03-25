from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.validators import MaxValueValidator

from .choices import METHODOLOGY_LIST, MODULES_LIST, INDUSTRIES_LIST

class Professional(models.Model):
    """
    Esse model é exclusivo para users com conta profissional, ele
    registra as informações que serão usadas no assessment.
    """
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        primary_key=True,
        editable=False
        )
    working_years = models.PositiveSmallIntegerField(null=True,
        blank=True,
        default=0,
        validators=[MaxValueValidator(38)])
    implementations = models.PositiveSmallIntegerField(null=True,
        blank=True,
        default=0,
        validators=[MaxValueValidator(38)])
    supports = models.PositiveSmallIntegerField(null=True,
        blank=True,
        default=0,
        validators=[MaxValueValidator(38)])
    occupation = models.CharField(max_length=200, null=True, blank=True)
    profile_pic = models.ImageField(
        upload_to='profile/',
        blank=True,
        null=True,
    )
    resume = models.FileField(
        upload_to='resume/', 
        blank=False, 
        null=True,
    )
    main_module = models.CharField(
        max_length=100,
        choices=MODULES_LIST,
        blank=True, 
        null=True,
    )
    secondary_module = models.CharField(
        max_length=100,
        choices=MODULES_LIST,
        blank=True, 
        null=True,
    )
    terciary_module = models.CharField(
        max_length=100,
        choices=MODULES_LIST,
        blank=True, 
        null=True,
    )
    main_industry = models.CharField(
        max_length=120,
        choices=INDUSTRIES_LIST,
        blank=True, 
        null=True,
    )
    secondary_industry = models.CharField(
        max_length=120,
        choices=INDUSTRIES_LIST,
        blank=True, 
        null=True,
    )
    terciary_industry = models.CharField(
        max_length=120,
        choices=INDUSTRIES_LIST,
        blank=True, 
        null=True,
    )
    methodology = models.CharField(
        max_length=70,
        choices=METHODOLOGY_LIST,
        blank=True, 
        null=True,
    )
    len_modules = models.IntegerField(default=0, null=True, blank=True)
    len_industries = models.IntegerField(default=0, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.occupation}'

    def get_absolute_url(self):
        return reverse('professional_profile', args=[str(self.user.id)])

    @property
    def modules(self):
        modules = [
            self.get_main_module_display(),
            self.get_secondary_module_display(),
            self.get_terciary_module_display(),
        ]
        while None in modules:
            modules.remove(None)

        string = ''
        for module in modules:
            string += f'{module}, '
        return (string.rstrip(', '), modules)

    @property
    def industries(self):
        industries = [
            self.get_main_industry_display(),
            self.get_secondary_industry_display(),
            self.get_terciary_industry_display(),
        ]
        while None in industries:
            industries.remove(None)

        string = ''
        for industry in industries:
            string += f'{industry}, '
        return (string.rstrip(', '), industries)

    def save(self, **kwargs):
        self.len_modules = len(self.modules[1])
        self.len_industries = len(self.industries[1])
        return super().save(**kwargs)