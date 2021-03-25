from django.forms import ModelForm

from .models import Professional

class ProfessionalUpdateForm(ModelForm):
    class Meta:
        model = Professional
        fields = (
            'working_years',
            'implementations',
            'supports',
            'occupation',
            'profile_pic',
            'resume',
            'main_module',
            'secondary_module',
            'terciary_module',
            'main_industry',
            'secondary_industry',
            'terciary_industry',
            'methodology',
            'bio',
        )
        labels = {
            'working_years': 'Anos de experiência',
            'implementations': 'Número de implantações',
            'supports': 'Número de suportes',
            'occupation': 'Cargo',
            'profile_pic': 'Foto de perfil',
            'resume': 'Currículo',
            'main_module': 'Módulo 1 (Ordene por experiência)',
            'secondary_module': 'Módulo 2',
            'terciary_module': 'Módulo 3',
            'main_industry': 'Indústria 1 (Ordene por experiência)',
            'secondary_industry': 'Indústria 2',
            'terciary_industry': 'Indústria 3',
            'methodology': 'Metodologia',
        }