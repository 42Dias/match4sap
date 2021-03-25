from django.db import models
from django.contrib.auth import get_user_model

class Score(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        primary_key=True,
        editable=False
        )
    working_years = models.IntegerField(default=0, null=True, blank=True)
    implementations = models.IntegerField(default=0, null=True, blank=True)
    supports = models.IntegerField(default=0, null=True, blank=True)
    modules = models.IntegerField(default=0, null=True, blank=True)
    industries = models.IntegerField(default=0, null=True, blank=True)
    methodology = models.IntegerField(default=0, null=True, blank=True)
    total = models.IntegerField(default=0, null=True, blank=True)
    rank = models.CharField(default=None, max_length=60, null=True, blank=True)

    def __str__(self):
        return f'{self.user}'

    def save(self, **kwargs):
        self.total = (
            self.working_years +
            self.implementations +
            self.supports +
            self.methodology +
            self.modules +
            self.industries
            )
        
        rank_table = {
            tuple(range(4)): None,
            tuple(range(4, 11)): 'INICIANTE',
            tuple(range(11, 21)): 'PLENO',
            tuple(range(21, 45)): 'SENIOR',
            tuple(range(44, 55)): 'EXPERT',
            tuple(range(55, 80)): 'SUPER EXPERT',
        }
        for performance in rank_table.keys():
            if self.total in performance:
                self.rank = rank_table[performance]
        return super().save(**kwargs)
