from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("<int:post_id>", views.post_detail_page, name="postdetail_page"),
    path("edit_post/<int:post_id>/", views.edit_post_page, name="editpost_page"),
    path("delete_post/<int:post_id>/", views.delete_post_page, name="deletepost_page"),
    path("create_post/", views.create_post_page, name="createpost_page"),
    path("search_blogs/", views.search_page, name="search_page"),
    ]