from django.conf.urls import url

from . import api

urlpatterns = [
    url(r'clients_workflow/user_dashboard_actions$', api.get_user_behavior, name='get_user_behavior'),
]