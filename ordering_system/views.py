# from django.shortcuts import render

from django.views.generic import ListView

from django.views.generic.edit import UpdateView


from django.contrib.auth.forms import AuthenticationForm

from ordering_system.models import DailySpecial

# Create your views here.


class DailySpecialListView(ListView):
    template_name = 'index.html'
    model = DailySpecial

    def get_context_data(self):
        context = super().get_context_data()
        context['login_form'] = AuthenticationForm
        return context


class DailySpecialUpdateView(UpdateView):
    model = DailySpecial
    success_url = "/"
    fields = ("name",)
