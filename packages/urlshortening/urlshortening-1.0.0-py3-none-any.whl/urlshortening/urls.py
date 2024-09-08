from django.urls import path, re_path
from django.conf import settings

from urlshortening.views import get_full_link, get_short_link, get_redirect, invalidate

urlpatterns = [
    path('expand/<path:short_id>/', get_full_link),
    path('short/', get_short_link),
    path('invalidate/', invalidate),
    re_path(r'^{}/expand/(?P<short_id>.+)/$'.format(settings.REDIRECT_PREFIX), get_redirect)
]
