from django.urls import path
from . views import log_view

urlpatterns = [
    path('', log_view, name='log_list'),
]
