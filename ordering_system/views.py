# from django.shortcuts import render

from django.views.generic import ListView

from django.views.generic.edit import UpdateView, CreateView, DeleteView

from django.contrib.auth.forms import AuthenticationForm

from ordering_system.models import DailySpecial, Profile, MenuItem, Order, OrderItem
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from ordering_system.mixins import OwnerAccessMixin, NotChefMixin, NotServerMixin

from extra_views import InlineFormSet, UpdateWithInlinesView, CreateWithInlinesView

from django.shortcuts import get_object_or_404

from django.shortcuts import render_to_response

# Create your views here.


class OrderItemInline(InlineFormSet):
    model = OrderItem
    extra = 5
    fields = ['quantity', 'menuitem']


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


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    login_url = '/login/'

    def get_queryset(self):
        if self.request.user.profile.is_owner:
            return Order.objects.all()
        else:
            return Order.objects.filter(paid=False)


class OrderDetailView(LoginRequiredMixin, NotChefMixin, UpdateWithInlinesView):
    model = Order
    inlines = [OrderItemInline]
    fields = ['table_number', 'paid']
    template_name = 'ordering_system/order_detail.html'
    success_url = reverse_lazy("order_list_view")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['object'] = Order.objects.get(id=pk)
        orderitem_obj = OrderItem.objects.filter(order=pk)
        total = 0
        for item in orderitem_obj:
            total += (item.quantity * item.menuitem.price)
        context['total'] = total
        return context


class OrderCreateView(LoginRequiredMixin, CreateWithInlinesView):
    model = Order
    inlines = [OrderItemInline]
    success_url = "/"
    fields = ('table_number', 'paid')


class OrderItemListView(LoginRequiredMixin, NotServerMixin, ListView):
    model = OrderItem
    login_url = '/'

    def get_queryset(self):
        if self.request.user.profile.is_owner:
            return OrderItem.objects.all()
        else:
            return OrderItem.objects.filter(prepared=False)


class OrderItemUpdateView(LoginRequiredMixin, UpdateView):
    model = OrderItem
    success_url = reverse_lazy("order_item_list_view")
    fields = ("prepared",)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.prepared = True
        return super().form_valid(form)
