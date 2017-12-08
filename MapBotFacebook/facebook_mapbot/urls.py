from django.conf.urls import url
from django.conf.urls import include
from .views import mapbotView
urlpatterns = [url(r'^mapbotwebhook/', mapbotView.as_view())]
