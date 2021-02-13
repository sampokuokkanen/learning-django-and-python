from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
import uuid

class Token(models.Model):
    email = models.EmailField()
    uid = models.UUIDField(default=uuid.uuid4)


class UserManager(BaseUserManager):

    def create_user(self, email):
        User.objects.create(email=email)

    def create_superuser(self, email, password):
        self.create_user(email)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email', 'height']

    objects = UserManager()

    @property
    def is_staff(self):
        return self.email == 'sampo.kuokkanen@harakka.jp'

    @property
    def is_active(self):
        return True
