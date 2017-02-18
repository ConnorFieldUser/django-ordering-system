# from django.shortcuts import render

from django.views.generic import ListView

from django.views.generic.edit import UpdateView, CreateView

from django.contrib.auth.forms import AuthenticationForm

from ordering_system.models import DailySpecial, Profile
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy

from ordering_system.mixins import OwnerAccessMixin


# Create your views here.


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = "/"


class ProfileUpdateView(UpdateView):
    template_name = "profile_update.html"
    fields = ("access_level",)
    success_url = reverse_lazy("profile_update_view")

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class DailySpecialListView(ListView):
    template_name = 'index.html'
    model = DailySpecial

    def get_context_data(self):
        context = super().get_context_data()
        context['login_form'] = AuthenticationForm
        return context


class DailySpecialUpdateView(OwnerAccessMixin, UpdateView):
    model = DailySpecial
    success_url = "/"
    fields = ("name", "price")
