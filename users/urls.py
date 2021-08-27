from django.urls import path

from .views import UserSignupView, TermosView

urlpatterns = [
    path('signup', UserSignupView.as_view(), name='signup_pro'),
    path('termos', TermosView.as_view(), name='termos'),
]