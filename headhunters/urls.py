from django.urls import path

from .views import (
    HeadhunterProfilePageView, ConnectionFormPageView, ConnectionResultsView,
    TokensFormView)

urlpatterns = [
    # Página do perfil do Headhunter.
    path('<uuid:pk>', 
        HeadhunterProfilePageView.as_view(), name='headhunter_profile'),

    # Página do formulário de conexão.
    path('connection_form', 
        ConnectionFormPageView.as_view(), name='connection_form'),

    # Página que mostra os resultados da conexão.
    path('connection/<uuid:pk>',
        ConnectionResultsView.as_view(), name='connection'),

    path('tokens_form',
        TokensFormView.as_view(), name='tokens_form'),
]