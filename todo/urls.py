from django.urls import path

from . import views

app_name = "todo"

urlpatterns = [
    path("", views.index, name="index"),
	path("home/", views.home, name="home"),
	path('signup/', views.signup, name='signup'),
	path("users/<int:pk>/", views.UserDetailView.as_view(), name="users_detail"),
	path("users/<int:pk>/update/", views.UserUpdateView.as_view(), name="users_update"),
	path("lists/", views.ListListView.as_view(), name="lists_list"),
	path("lists/create/", views.ListCreateView.as_view(), name="lists_create"),
	path("lists/<int:pk>/", views.ListDetailView.as_view(), name="lists_detail"),
	path("lists/<int:pk>/update/", views.ListUpdateView.as_view(), name="lists_update"),
	path("lists/<int:pk>/delete/", views.ListDeleteView.as_view(), name="lists_delete"),
]
