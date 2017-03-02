from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy


class OwnerAccessMixin(UserPassesTestMixin):
    login_url = '/'
    redirect_field_name = "None"

    def test_func(self):
        return self.request.user.profile.access_level == "o"


class NotChefMixin(UserPassesTestMixin):
    login_url = reverse_lazy('daily_special_list_view')
    redirect_field_name = "None"

    def test_func(self):
        return self.request.user.profile.access_level != "c"
