from django.conf.urls import include, url
from apps.operations.views import AddFavorView

urlpatterns = [
    url(r'^fav/$', AddFavorView.as_view(), name='fav'),
]