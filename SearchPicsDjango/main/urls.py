from django.conf.urls import url

from .views import *

urlpatterns = [

    url(r'search/(?P<phrase>\w+)/$', SearchView.as_view()),
    url(r'^$', MainView.as_view()),
]