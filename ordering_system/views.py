# from django.shortcuts import render

from django.views.generic import ListView

from django.views.generic.edit import UpdateView, CreateView, DeleteView

from django.contrib.auth.forms import AuthenticationForm

from ordering_system.models import DailySpecial, Profile, MenuItem
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from ordering_system.mixins import OwnerAccessMixin


# Create your views here.


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = "/"


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "profile_update.html"
    fields = ("access_level",)
    success_url = reverse_lazy("profile_update_view")
    login_url = '/login/'

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


class MenuItemListView(ListView):
    model = MenuItem


class MenuItemCreateView(OwnerAccessMixin, CreateView):
    model = MenuItem
    success_url = reverse_lazy("menu_item_list_view")
    fields = ('name', 'description', 'price')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super().form_valid(form)


class MenuItemDeleteView(OwnerAccessMixin, DeleteView):
    model = MenuItem
    success_url = reverse_lazy('menu_item_list_view')


class MenuItemUpdateView(OwnerAccessMixin, UpdateView):
    model = MenuItem
    success_url = reverse_lazy("menu_item_list_view")
    fields = ('name', 'description', 'price')
