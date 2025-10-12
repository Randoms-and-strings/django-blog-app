from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("new-user/", views.register, name="register_page"),
    path("existing-user/", views.login_view, name="login_page"),
    path("user-sign-out/", views.logout_view, name="logout_page"),
    path("existing-user-profile/<int:user_id>/", views.profile, name="profile_page"),
path("edit-existing-user-profile/<int:user_id>/", views.edit_profile, name="edit_profile_page"),
]