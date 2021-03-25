from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Score
from professionals.models import Professional
from users.models import CustomUser

def working_years_score(atribute=None):
    if atribute == None:
        score = 0
    else:
        score_table = {
            tuple(range(2)): 2,
            tuple(range(2, 5)): 6,
            tuple(range(5, 11)): 10,
            tuple(range(11, 21)): 14,
            tuple(range(21, 40)): 20
        }
        for performance in score_table.keys():
            if atribute in performance:
                score = score_table[performance]
    return score

def implementations_score(atribute=None):
    if atribute == None or atribute == 0:
        score = 0
    else:
        score_table = {
            tuple(range(1, 4)): 2,
            tuple(range(4, 8)): 8,
            tuple(range(8, 10)): 10,
            tuple(range(10, 30)): 12
        }
        for performance in score_table.keys():
            if atribute in performance:
                score = score_table[performance]
    return score

def supports_score(atribute=None):
    if atribute == None or atribute == 0:
        score = 0
    else:
        score_table = {
            tuple(range(1, 4)): 2,
            tuple(range(4, 8)): 4,
            tuple(range(8, 10)): 8,
            tuple(range(10, 30)): 10
        }
        for performance in score_table.keys():
            if atribute in performance:
                score = score_table[performance]
    return score

def modules_score(atribute=None):
    if atribute:
        if atribute == 0:
            score = 1
        elif len(atribute) == 1:
            score = 3
        elif len(atribute) == 2:
            score = 5
        elif len(atribute) == 3:
            score = 8
        return score
    else:
        return 0

def industries_score(atribute=None):
    if atribute:
        if atribute == 0:
            score = 1
        elif len(atribute) == 1:
            score = 3
        elif len(atribute) == 2:
            score = 5
        elif len(atribute) == 3:
            score = 8
        return score
    else:
        return 0

def methodology_score(atribute=None, working_years=None):
    if atribute == 'ASAP' or atribute == None:
        score = 0
    else:
        score_table = {
            tuple(range(2)): 2,
            tuple(range(2, 5)): 3,
            tuple(range(5, 9)): 4,
            tuple(range(9, 40)): 5
        }
        for performance in score_table.keys():
            if working_years in performance:
                score = score_table[performance]
    return score

@receiver(post_save, sender=Professional)
def create_user_score(sender, instance, created, **kwargs):
    if created:
        score = Score.objects.create(user=instance.user)
        score.working_years = working_years_score(instance.working_years)
        score.implementations = implementations_score(instance.implementations)
        score.supports = supports_score(instance.supports)

        try:
            score.modules = modules_score(instance.len_modules)
        except:
            score.modules = modules_score(None)

        try:
            score.industries = industries_score(instance.len_modules)
        except:    
            score.industries = industries_score(None)

        score.methodology = methodology_score(
            instance.methodology,
            instance.working_years
        )
        score.save()
    else:
        score = Score.objects.filter(user=instance.user)
        score.update(
            working_years=working_years_score(instance.working_years),
            implementations=implementations_score(instance.implementations),
            supports=supports_score(instance.supports),
            modules=modules_score(instance.modules[1]),
            industries=industries_score(instance.industries[1]),
            methodology=methodology_score(
            instance.methodology,
            instance.working_years
            )
        )
        Score.objects.get(user=instance.user).save()