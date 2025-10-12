from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
def user_directory_path(instance, filename):
    # This won't really be used now, but it prevents migration errors
    return f'profile_pics/{filename}'


class ProfileDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=120, default="enter_your_full_name")
    birthday = models.DateField(default=date.today)
    image = models.ImageField(default="profile_pics/default.jpg", upload_to= "profile_pics")

