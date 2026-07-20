from django.contrib.auth.views import LogoutView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView
from django.urls import path

from .forms import LoginForm
from .views import ProfileView, RegisterView, UserLoginView, UserPasswordChangeView

app_name = "accounts"

urlpatterns = [
    path("login/", UserLoginView.as_view(authentication_form=LoginForm), name="account_login"),
    path("logout/", LogoutView.as_view(), name="account_logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("password-change/", UserPasswordChangeView.as_view(), name="password_change"),
    path("password-reset/", PasswordResetView.as_view(template_name="accounts/password_reset_form.html"), name="password_reset"),
    path("password-reset/done/", PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_done"),
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    path("password-reset/complete/", PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
]
