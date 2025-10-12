from functools import wraps
from .models import BlogPost
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.models import User

from . import views
from django.shortcuts import redirect


def protect_route_decorator_wrapper(function):
    ##post_id in views is a kwargs, args didnt work
    wraps(function)

    def wrapped_function(request, **kwa):
        for items in kwa:
            if items == "post_id":
                the_blog_post = BlogPost.objects.get(id=kwa["post_id"])
                if request.user.is_authenticated and the_blog_post.author == request.user:
                    return function(request, **kwa)
                else:
                    return HttpResponseNotFound("<h1>YOU DO NOT HAVE PERMISSION<br/>"
                                                "TO ACCESS THIS PAGE</h1>")

            elif items == "user_id":
                the_user = User.objects.get(id=kwa["user_id"])
                if request.user.is_authenticated and kwa["user_id"] == request.user.id:
                    return function(request, **kwa)
                else:
                    return HttpResponseNotFound("<h1>YOU DO NOT HAVE PERMISSION<br/>"
                                                "TO ACCESS THIS PAGE</h1>")

        # if request.user.is_authenticated and the_blog_post.author == request.user:
        #     return function(request, **kwa)
        # else:
        #     return HttpResponseNotFound("<h1>YOU DO NOT HAVE PERMISSION<br/>"
        #                                 "TO ACCESS THIS PAGE</h1>")

    return wrapped_function