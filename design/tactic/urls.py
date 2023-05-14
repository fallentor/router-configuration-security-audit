from django.urls import path
from . views import tacticGroup_list, tactic_list, delete_tactic_group, delete_tactic, tactic_edit, edit_tactic

urlpatterns = [
	path('tacticGroup_list/', tacticGroup_list, name='tacticGroup_list'),
	path('tactic_list/', tactic_list, name='tactic_list'),
	path('delete_tactic_group/', delete_tactic_group, name="delete_tactic_group"),
	path('delete_tactic/', delete_tactic, name="delete_tactic"),
	path('tactic_edit/', tactic_edit, name="tactic_edit"),
	path('edit_tactic/', edit_tactic, name="edit_tactic"),
]