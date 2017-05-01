from django.conf.urls import url

from .views import commandRequest

urlpatterns = [
    url(r'^cmd/', commandRequest),
]
