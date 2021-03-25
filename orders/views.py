import stripe

from django.conf import settings
from django.shortcuts import render
from django.views.generic.base import TemplateView

from headhunters.models import Headhunter

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

class OrdersPageView(TemplateView):
    template_name = 'orders/purchase.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stripe_key'] = settings.STRIPE_TEST_PUBLISHABLE_KEY
        return context

    
def charge(request):
    if request.method == 'POST':
        u = request.user
        charge = stripe.Charge.create(
            amount=1500,
            currency='usd',
            description='Puchase Connection Token',
            source=request.POST['stripeToken']
        )
        new_tokens = u.headhunter.tokens + 1
        u.headhunter.tokens = new_tokens
        new_total = u.headhunter.tokens_total + 1
        Headhunter.objects.filter(user=u).update(
            tokens=new_tokens,
            tokens_total=new_total,
        )
        return render(request, 'orders/charge.html')
