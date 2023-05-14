from django.urls import path
from . views import device_list_view, device, delete_device, device_add, add_device, search_device

urlpatterns = [
    # path('', device_list_view, name='device_list_view')
    path('', device, name='device'),
    path('delete-device/', delete_device, name='delete_device'),
    path('device_add/', device_add, name='device_add'),
    path('add_device/', add_device, name='add_device'),
    path('search_device/', search_device, name="search_device"),
    
]
