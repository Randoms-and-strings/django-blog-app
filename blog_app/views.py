from django.contrib.auth.decorators import login_required
from django.contrib.messages import success
from django.shortcuts import render, redirect
from .models import BlogPost
from .forms import EditBlog
from .my_decorators import  protect_route_decorator_wrapper
from django.core.paginator import Paginator
# Create your views here.
def home_page(request):

    data = {

    }

    all_posts = BlogPost.objects.all()
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    data["page_obj"] = page_obj

    return render(request, "blog/index.html", data)

def post_detail_page(request, post_id):
    data = {
        "blog_details": BlogPost.objects.get(id=post_id)
    }
    return render(request, "blog/post_detail.html", data)

@protect_route_decorator_wrapper
@login_required
def edit_post_page(request, post_id):
    the_post = BlogPost.objects.get(id=post_id)
    if request.method == "POST":
        form = EditBlog(request.POST, instance=the_post)
        if form.is_valid():
            form.save()
            success(request, "Your post has been updated successfully")
            return redirect("postdetail_page", post_id)

    form = EditBlog(instance=the_post)
    return render(request, "blog/edit_post.html", {"form":form})

@protect_route_decorator_wrapper
@login_required
def delete_post_page(request, post_id):
    the_post = BlogPost.objects.get(id=post_id)

    if request.method == "POST":
        the_post.delete()
        success(request, "your post has been deleted successfully")
        return redirect("home_page")

    data = {
        "the_post": the_post,
    }
    return render(request, "blog/delete_post.html", data)


@login_required
def create_post_page(request):
    edit_blog = EditBlog()

    if request.method == "POST":
        edit_blog = EditBlog(request.POST)
        if edit_blog.is_valid():
            # edit_blog.save()
            title = edit_blog.cleaned_data["title"]
            subtitle = edit_blog.cleaned_data["subtitle"]
            content = edit_blog.cleaned_data["content"]
            new_post = BlogPost.objects.create(title=title, subtitle=subtitle, content=content, author=request.user).save()
            success(request, "your post has been created")
            return redirect("home_page")
        else:
            edit_blog = EditBlog(request.POST)

    data = {
        "create_post_form": edit_blog,
            }
    return render(request, "blog/create_post.html", data)

# def error_page(request, exception=None):
#
#     return render(request, "blog/error_page.html", status=404)