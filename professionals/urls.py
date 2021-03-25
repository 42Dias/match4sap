from django.urls import path

from .views import (
    ProfessionalProfilePageView, ProfessionalUpdateFormView, 
    ProfessionalCreateFormView, PreProfessionalProfilePageView,
    ProfessionalResultProfileView)

urlpatterns = [
    # Página do perfil do profissional.
    path('pre/<uuid:pk>',
        PreProfessionalProfilePageView.as_view(), name='pre_professional_profile'),

    # Página do perfil do profissional.
    path('<uuid:pk>',
        ProfessionalProfilePageView.as_view(), name='professional_profile'),

    path('profile_result/<uuid:pk>',
        ProfessionalResultProfileView.as_view(), name='profile_result'),

    # Página de criação do perfil do profissional.
    path('professional_create_form',
        ProfessionalCreateFormView.as_view(), name='professional_create_form'),

    # Página de formulário de update dos dados do profissional.
    path('professional_update_form',
        ProfessionalUpdateFormView.as_view(), name='professional_update_form'),
]