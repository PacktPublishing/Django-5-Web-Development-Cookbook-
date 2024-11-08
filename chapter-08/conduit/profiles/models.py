from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if name is None:
            raise TypeError("Users must have a name.")

        if email is None:
            raise TypeError("Users must have an email address.")

        user = self.model(email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, password=None):
        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser):

    email: str = models.EmailField("Email Address", unique=True)
    name: str = models.CharField("Name", max_length=60)
    bio: str = models.TextField(blank=True)
    image: str | None = models.URLField(null=True, blank=True)
    is_active: bool = models.BooleanField(default=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"<User: {self.email}>"

    def get_full_name(self) -> str:
        return self.name

    linkedin_url: str = models.URLField(blank=True)

    followers = models.ManyToManyField(
        "self", related_name="followees", symmetrical=False
    )

    objects = UserManager()
