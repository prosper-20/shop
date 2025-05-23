from django.urls import path
from .views import (
    create_user,
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
    CustomPasswordChangeView,
    CustomPasswordChangeDoneView,
)

urlpatterns = [
    # Password reset
    path("create/", create_user, name="create_user"),
    path("password-reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path(
        "password-reset/done/",
        CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset/confirm/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # Password change (for logged-in users)
    path(
        "password-change/", CustomPasswordChangeView.as_view(), name="password_change"
    ),
    path(
        "password-change/done/",
        CustomPasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
]
