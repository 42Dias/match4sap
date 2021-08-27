from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from allauth.account.views import SignupView

from .forms import CustomUserCreationForm
from headhunters.models import Headhunter

class UserSignupView(SignupView):
    template_name = 'account/signup.html'
    form_class = CustomUserCreationForm

    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret        

    def form_valid(self, form):
        if form.is_valid():
            user = form.save(self.request)
            if 'hh_button' in self.request.POST:
                permission = Permission.objects.get(name='Can access headhunter data')
                user.user_permissions.add(permission)            
                user.is_headhunter = True
                Headhunter.objects.create(user=user)
        return super().form_valid(form)

    def get_success_url(self):
        if 'hh_button' in self.request.POST:
            success_url = reverse_lazy('connection_form')
        else:
            success_url = reverse_lazy('professional_create_form')
        return success_url

class TermosView(SignupView):
    template_name = 'account/termos.html'
    form_class = CustomUserCreationForm
    login_url = 'account_login'
    # Captura o atual user.
    def get_termos(self):
        return reverse_lazy('termos')