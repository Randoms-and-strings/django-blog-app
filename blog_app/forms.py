from django.forms import ModelForm
from .models import BlogPost

class EditBlog(ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "subtitle", "content"]

# class CreatePostForm(ModelForm):
#     class Meta:
#         model = BlogPost
#         fields = []