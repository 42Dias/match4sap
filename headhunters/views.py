import stripe

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import ConnectionForm, TokensForm
from .models import Job, Headhunter
from users.models import CustomUser

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

class HeadhunterProfilePageView(
    LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = 'headhunter/profile.html'
    model = get_user_model()
    login_url = 'account_login'
    permission_required = 'headhunters.special_status'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_key'] = settings.STRIPE_TEST_PUBLISHABLE_KEY
        return context


class ConnectionFormPageView(
    LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'headhunter/connection_form.html'
    form_class = ConnectionForm
    login_url = 'account_login'
    permission_required = 'headhunters.special_status'

    def form_valid(self, form):
        """Salva o user atual como user do objeto."""
        f = form.save(commit=False)
        u = self.request.user
        f.author = u
        f.save()

        new_tokens = u.headhunter.tokens - 1
        u.headhunter.tokens = new_tokens
        Headhunter.objects.filter(user=u).update(tokens=new_tokens)
        return super().form_valid(form)


class ConnectionResultsView(
    LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = 'headhunter/connection.html'
    model = Job
    login_url = 'account_login'
    permission_required = 'headhunters.special_status'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = CustomUser.objects.exclude(is_headhunter=True)
        query = query.filter(state=self.object.state)
        if self.object.methodology:
            query = query.filter(
                professional__methodology=self.object.methodology
            )
        if self.object.modules:
            query = query.filter(
                professional__main_module=self.object.modules
                )
        if self.object.industries:
            query = query.filter(
                professional__main_industry=self.object.industries
            )
        if self.object.working_years:
            query = query.filter(
                Q(professional__working_years=self.object.working_years - 1) | 
                Q(professional__working_years=self.object.working_years) | 
                Q(professional__working_years=self.object.working_years + 1)
            )
        context['query'] = query[:15]
        context['stripe_key'] = settings.STRIPE_TEST_PUBLISHABLE_KEY
        return context

    
class TokensFormView(
    LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'headhunter/tokens_form.html'
    form_class = TokensForm
    login_url = 'account_login'
    permission_required = 'headhunters.special_status'

    def get_object(self, queryset=None):
        obj = Headhunter.objects.get(user=self.request.user)
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        user = self.request.user
        pk = user.id
        return reverse_lazy('headhunter_profile', kwargs={'pk': pk})