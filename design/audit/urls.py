from django.urls import path
from . views import audit_list, report_export, export_configuration, export, audit_, audit_result_show, delete_, visualization

urlpatterns = [
	path('audit_list/', audit_list, name='audit_list'),
	path('report_export/', report_export, name='report_export'),
	path('export_configuration/', export_configuration, name='export_configuration'),
	path('export/', export, name='export'),
	path('audit_', audit_, name='audit_'),
	path('audit_result_show/', audit_result_show, name='audit_result_show'),
	path('delete_/', delete_, name="delete_"),
	path('visualization/', visualization, name="visualization"),
]