from django.urls import include, path
from profiles import views
from rest_framework.routers import DefaultRouter

profile_router = DefaultRouter(trailing_slash=False)
profile_router.register(r"profiles", views.ProfileDetailView)

urlpatterns = [
    path("users/login/", views.login, name="account-login"),
    path("users", views.account_registration, name="register"),
    path("user", views.UserView.as_view(), name="user"),
    path("", include(profile_router.urls)),
]
