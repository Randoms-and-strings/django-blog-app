from django.contrib.auth.decorators import login_required
from django.contrib.messages import success
from django.shortcuts import render, redirect
from .models import BlogPost
from .forms import EditBlog
from .my_decorators import  protect_route_decorator_wrapper
from django.core.paginator import Paginator
from elasticsearch import Elasticsearch, AuthorizationException, NotFoundError
from dotenv import load_dotenv
import os

load_dotenv()
# client = Elasticsearch(f"http://{os.getenv("ELASTIC_HOSTNAME_DOCKER")}:{os.getenv("ELASTIC_PORT")}",
#                        basic_auth=(os.getenv("ELASTIC_USER"), os.getenv("ELASTIC_PASSWORD")))
client = Elasticsearch(f"https://{os.getenv("ELASTIC_HOSTNAME_DOCKER")}:{os.getenv("ELASTIC_PORT")}")
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

def search_page(request):

    if request.method == "POST":

        search_word = request.POST.get("keyword")
        search_filter = request.POST.get("search_by").lower()

        if search_filter == "title":
            search = client.search(index="blog_posts", query={
                "match": {
                    "title": search_word,
                }
            })
            context = {"data": search["hits"]["hits"]}

        elif search_filter == "author":
            search = client.search(index="blog_posts", query={
                "match": {
                    "author": search_word,
                }
            })
            context = {"data": search["hits"]["hits"]}


        else:
            search = client.search(index="blog_posts", query={
                "multi_match": {
                    "query": search_word,
                    "fields": [ "title", "author", "content" ],

                }
            })
            # print(search)

            context = {"data": search["hits"]["hits"]}
            # {'took': 10, 'timed_out': False, '_shards': {'total': 1, 'successful': 1, 'skipped': 0, 'failed': 0},
            #  'hits': {'total': {'value': 1, 'relation': 'eq'}, 'max_score': 0.7721133,
            #           'hits': [{'_index': 'blog_posts', '_id': '10', '_score': 0.7721133,
            #                     '_source':
            #                         {'title': 'Elastic Search API', 'subtitle': 'Testing Python Client', 'content': 'this is a dummy post'}}]}}


            # search["hits"]["hits"][0]["_source"]["title"]
        return render(request, "blog/search.html", context)


    elif request.method == "GET":
        return render(request, "blog/search.html")

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

            client.update(
                index="blog_posts",
                id=post_id,
                doc={
                    "title": request.POST.get("title"),
                    "subtitle": request.POST.get("subtitle"),
                    "content": request.POST.get("content"),
                    "author": request.user.username
                }
            )
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
        try:
            client.delete(index="blog_posts", id=post_id)
        except NotFoundError:
            print("the file was nevr saved to es for some reason")
        else:
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
            new_blog_id = BlogPost.objects.get(title=title)


            ###add post to ES here
            if client.indices.exists(index="blog_posts"):
                client.index(
                    index="blog_posts",
                    id=new_blog_id.id,
                    document={
                        "title": title,
                        "subtitle": subtitle,
                        "content": content,
                        "author": request.user.username
                    }
                )
            else:
                client.indices.create(index="blog_posts")
                client.index(
                    index="blog_posts",
                    id=new_blog_id.id,
                    document={
                        "title": title,
                        "subtitle": subtitle,
                        "content": content,
                    }
                )

            ######
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
