from django.contrib.auth.mixins import UserPassesTestMixin


class OwnerAccessMixin(UserPassesTestMixin):
    login_url = '/'
    redirect_field_name = "None"

    def test_func(self):
        return self.request.user.profile.access_level == "o"
