from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/')
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_user_permissions", blank=True)

    def __str__(self):
        return self.username


class Notes(models.Model):
    description = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="note")
