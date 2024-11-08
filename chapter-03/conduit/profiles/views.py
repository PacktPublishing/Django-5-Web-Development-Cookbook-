from django.contrib.auth import authenticate
from rest_framework import status, views, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView, LoginView
from .forms import UserRegistrationForm

from .models import User
from .serializers import ProfileSerializer, UserSerializer

import logging
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import views as auth_views

logger = logging.getLogger(__name__)
# Create your views here.


@api_view(["POST"])
def account_registration(request):
    try:
        user_data = request.data.get("user")

        print("User Data: ", user_data)

        serializer = UserSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        print("after Serializer Data: ", serializer.data)
        return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)

    except Exception as e:
        print("Error: ", e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    try:
        logger.info(f"login() request.data: {request.data}")
        user_data = request.data.get("user")
        logger.info(f"login() user_data: {user_data}")
        user = authenticate(email=user_data["email"], password=user_data["password"])
        logger.info(f"login() user: {user}")
        serializer = UserSerializer(user)
        jwt_token = RefreshToken.for_user(user)
        serializer_data = serializer.data
        serializer_data["token"] = str(jwt_token.access_token)
        response_data = {
            "user": serializer_data,
        }
        return Response(response_data, status=status.HTTP_202_ACCEPTED)

    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None, pk=None):

        user = request.user
        data = request.data
        serializer = UserSerializer(instance=user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetailView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "name"
    http_method_names = ["get", "post", "delete"]

    def get_permissions(self):
        if self.action == "list":
            return [
                IsAuthenticatedOrReadOnly(),
            ]
        return super().get_permissions()

    def list(self, request, name=None, *args, **kwargs):
        try:
            profile = User.objects.get(name=name)
            serializer = self.get_serializer(profile)
            return Response({"profile": serializer.data})

        except Exception:
            return Response({"errors": {"body": ["Invalid User"]}})

    @action(detail=True, methods=["post", "delete"])
    def follow(self, request, name=None, *args, **kwargs):
        if request.method == "POST":

            profile = self.get_object()
            follower = request.user
            if profile == follower:
                return Response(
                    {"errors": {"body": ["Invalid follow Request"]}},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            profile.followers.add(follower)
            serializer = self.get_serializer(profile)
            return Response({"profile": serializer.data})

        elif request.method == "DELETE":

            profile = self.get_object()
            follower = request.user
            if profile == follower:
                return Response(
                    {"errors": {"body": ["Invalid follow Request"]}},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not profile.followers.filter(pk=follower.id).exists():
                return Response(
                    {"errors": {"body": ["Invalid follow Request"]}},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            profile.followers.remove(follower)
            serializer = self.get_serializer(profile)
            return Response({"profile": serializer.data})


class UserRegistrationView(FormView):
    template_name = "profiles/register.html"
    form_class = UserRegistrationForm
    success_url = "/login/"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        return super(UserRegistrationView, self).form_valid(form)


class ModularLoginView(LoginView):
    template_name = "profiles/login.html"
    redirect_authenticated_user = True
    next_page = "/profile/"


class ModularLogoutView(LogoutView):
    next_page = "/account/login/"


# create a basic view for profile using templates/profile only if logged in


class ProfileView(TemplateView):
    template_name = "profiles/profile.html"
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        logger.info(f"ProfileView.get() request.user: {request.user}")
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_context_data(self, **kwargs):
        logger.info(f"ProfileView.get_context_data() kwargs: {kwargs}")
        context = super().get_context_data(**kwargs)
        logger.info(f"ProfileView.get_context_data() user: {self.request.user}")
        logger.info(f"bio: {self.request.user.bio}, image: {self.request.user.image}")
        context["profile"] = self.request.user
        return context


class ModularPasswordResetDoneView(TemplateView):
    template_name = "profiles/password_reset_complete.html"


class ModularPassordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "profiles/password_reset_confirm.html"


class ModularPasswordResetView(auth_views.PasswordResetView):
    template_name = "profiles/password_reset_form.html"
    email_template_name = "profiles/password_reset_email.html"
    success_url = "/password_reset/done/"
    from_email = "bogdan@codeswiftr.com"

    def form_valid(self, form):
        logger.info(f"form_valid() form")
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        logger.debug(f"reset password  opts: {opts}")
        form.save(**opts)
        logger.debug(f"reset password  email sent")
        return super().form_valid(form)


class ModularPasswordResetCompleteView(TemplateView):
    template_name = "profiles/password_reset_complete.html"


# class ModularTwoFactorSetupView(TwoFactorSetupView):
#     template_name = "profiles/two_factor_setup.html"
#     success_url = "/profiles/profile/"
