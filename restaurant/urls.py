"""restaurant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from ordering_system.views import DailySpecialListView, DailySpecialUpdateView, ProfileUpdateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^', include('django.contrib.auth.urls')),
    url(r'^profile/update/$', ProfileUpdateView.as_view(), name="profile_update_view"),
    url(r'^$', DailySpecialListView.as_view(), name="daily_special_list_view"),
    url(r'^daily_special/(?P<pk>\d+)/update/$', DailySpecialUpdateView.as_view(), name="daily_special_update_view"),
]
