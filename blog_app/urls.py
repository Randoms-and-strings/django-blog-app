from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("blog/<int:post_id>", views.post_detail_page, name="postdetail_page"),
    path("blog/edit_post/<int:post_id>/", views.edit_post_page, name="editpost_page"),
    path("blog/delete_post/<int:post_id>/", views.delete_post_page, name="deletepost_page"),
    path("blog/create_post/", views.create_post_page, name="createpost_page"),

    ]