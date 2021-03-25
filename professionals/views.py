from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.db.models import Avg, Count, Q

from users.models import CustomUser

from .forms import ProfessionalUpdateForm
from .models import Professional
from .assessment import *

class PreProfessionalProfilePageView(LoginRequiredMixin, DetailView):
    """View que encaminha user para a criação do perfil."""
    template_name = 'professional/pre_profile.html'
    model = CustomUser
    login_url = 'account_login'


class ProfessionalProfilePageView(LoginRequiredMixin, DetailView):
    """View que detalha os dados do user."""
    template_name = 'professional/profile.html'
    model = CustomUser
    login_url = 'account_login'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        obj =self.object
        context.update(assessment(obj))
        return context


class ProfessionalResultProfileView(
    LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = 'professional/profile_result.html'
    model = CustomUser
    login_url = 'account_login'
    permission_required = 'headhunters.special_status'


class ProfessionalCreateFormView(LoginRequiredMixin, CreateView):
    """View usada para a criação de um objeto do model Professionals."""
    template_name = 'professional/professional_create_form.html'
    form_class = ProfessionalUpdateForm
    login_url = 'account_login'

    def form_valid(self, form):
        """
        Salva o user atual como user do objeto e cria um objeto
        no model Score, que será o responsável pelo assessment.
        """
        f = form.save(commit=False)
        f.user = self.request.user
        f.save()

        return super().form_valid(form)


class ProfessionalUpdateFormView(LoginRequiredMixin, UpdateView):
    template_name = 'professional/professional_update_form.html'
    form_class = ProfessionalUpdateForm
    login_url = 'account_login'

    # Captura o atual user.
    def get_object(self, queryset=None):
        obj = Professional.objects.get(user=self.request.user)
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ProfessionalUpdateFormView, self).post(request, *args, **kwargs)

    # Retorna a URL para o redirect após validar o form.
    def get_success_url(self):
        user = self.request.user
        pk = user.id
        return reverse_lazy('professional_profile', kwargs={'pk': pk})