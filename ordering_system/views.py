# from django.shortcuts import render

from django.views.generic import TemplateView

from django.contrib.auth.forms import AuthenticationForm


# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['login_form'] = AuthenticationForm
        return context
