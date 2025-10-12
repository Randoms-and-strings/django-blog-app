from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success, error
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, EditProfile, EditAdminDetails
from .models import ProfileDetails
from django.urls import reverse
import os
from blog_app.models import BlogPost
from blog_app.my_decorators import protect_route_decorator_wrapper
from django.contrib.auth.models import User
from django.conf import settings



# Create your views here.
def register(request):
    """REGISTER PAGE"""
    # register_form = RegisterForm()
    data = {
        "register_form": RegisterForm(),
    }

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            success(request, "Your account has been created successfully, Please login.")
            return redirect('login_page')
        else:
            data["register_form"] = RegisterForm(request.POST)

    return render(request, "users/register.html", data)

def login_view(request):
    """LOGIN PAGE """
    data = {
        "login_form": LoginForm(),

    }

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username= request.POST["email"]

            password= request.POST["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)   #used Newuser4 Testing321
                success(request, "Your login was successful")
                return redirect('home_page')
        else:
            data["login_form"] = LoginForm(request.POST)
            error(request, "please fix the following errors")
            return redirect("login_page")

    return render(request, "users/login.html", data)

def logout_view(request):
    logout(request)
    success(request, "you have been logged out")
    return redirect("login_page")

@login_required
def profile(request, user_id):
    """PAGE SHOWING THE USER'S DETAILS"""

    user_posts = BlogPost.objects.filter(author=user_id)
    the_profile = User.objects.get(id=user_id)
    paginator = Paginator(user_posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "users/profile.html", {"page_obj": page_obj, "user_profile":the_profile})

@protect_route_decorator_wrapper
@login_required
def edit_profile(request, user_id):
    """TO EDIT THE USER'S PROFILE"""
    data = {
        "user_form": EditAdminDetails(instance=request.user),
        "details_form": EditProfile(instance=request.user.profiledetails),
    }

    if request.method == "POST":
        form = EditAdminDetails(request.POST, instance=request.user)
        form2 = EditProfile(request.POST, request.FILES, instance=request.user.profiledetails)
        if form.is_valid() and form2.is_valid():
            user_details = ProfileDetails.objects.get(user=request.user)  #gets a user detail from the db
            removed_image_name = user_details.image.name #gets the name of the image to be removed
            removed_image_path = user_details.image.path #gets the path to the image to be changed for deletion

            form.save()  #saves the new details + new photo
            form2.save()

            if "default.jpg" not in removed_image_name: #checks the default image is not the normal default one to avoid deleting it
                os.remove(removed_image_path) #removes the old image from storage

            success(request, "Your user details have been updated successfully")
            return redirect("profile_page", user_id=user_id)
        else:
            data["user_form"] = EditAdminDetails(request.POST, request.FILES, instance=request.user)
            data["details_form"] = EditProfile(request.POST, instance=request.user)

    return render(request, "users/edit_profile.html", data)