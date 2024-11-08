from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if username is None:
            raise TypeError("Users must have a username.")

        if email is None:
            raise TypeError("Users must have an email address.")

        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, username, password=None):
        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(email, username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser):
    first_name = None
    last_name = None

    email: str = models.EmailField("Email Address", unique=True)
    username: str = models.CharField(max_length=60)
    bio: str = models.TextField(blank=True)
    image: str | None = models.URLField(blank=True)

    followers = models.ManyToManyField(
        "self", related_name="followees", symmetrical=False
    )
    # favorites = models.ManyToManyField('articles.Article', related_name='favorited_by')

    objects = UserManager()
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="profile_user_set",  # unique related_name
        related_query_name="profile_user",
    )

    # Modify the user_permissions relationship
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="profile_user_permission_set",  # unique related_name
        related_query_name="profile_user_permission",
    )

    def get_full_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.username

    def get_short_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name}"
        else:
            return self.username

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
