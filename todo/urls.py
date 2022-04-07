from django.urls import path

from . import views

app_name = "todo"

urlpatterns = [
    path("", views.index, name="index"),
	path("home/", views.home, name="home"),
	path('signup/', views.signup, name='signup'),
	path("users/<int:pk>/", views.UserDetailView.as_view(), name="users_detail"),
	path("users/<int:pk>/update/", views.UserUpdateView.as_view(), name="users_update"),
]
