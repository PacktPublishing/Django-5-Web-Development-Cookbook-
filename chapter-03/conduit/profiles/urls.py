from django.urls import include, path
from profiles import views
from rest_framework.routers import DefaultRouter
from .views import (
    ModularLoginView,
    ModularLogoutView,
    UserRegistrationView,
    ModularPasswordResetView,
    ModularPasswordResetCompleteView,
    ModularPassordResetConfirmView,
    ModularPasswordResetDoneView,
)
from django.contrib.auth import views as auth_views
from two_factor.urls import urlpatterns as tf_urls

profile_router = DefaultRouter(trailing_slash=False)
profile_router.register(r"profiles", views.ProfileDetailView)

urlpatterns = [
    path("api/users/login/", views.login, name="account-login"),
    path("api/users", views.account_registration, name="register"),
    path("api/user", views.UserView.as_view(), name="user"),
    # path("login/", ModularLoginView.as_view(), name="login"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("logout/", ModularLogoutView.as_view(), name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("password_reset/", ModularPasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        ModularPasswordResetDoneView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "reset/<uidb64>/<token>/",
        ModularPassordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        ModularPasswordResetDoneView.as_view(),
        name="password_reset_complete",
    ),
    path("", include(profile_router.urls)),
    path("", include(tf_urls)),
]
