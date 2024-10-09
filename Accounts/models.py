from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, unique=True)
    image = models.ImageField(upload_to='accounts/profile/',
                              default='accounts/profile/default/default_avatar.jpg')

    def __str__(self):
        return self.user.username

