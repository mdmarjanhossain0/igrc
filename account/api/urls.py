from django.urls import path

from account.api.views import (
    Login,
    send_otp_view,
    register_view
)
app_name = 'account_api'

urlpatterns = [
    path("login", Login.as_view()),
    path("send_otp/<mobile>", send_otp_view),
    path("register", register_view)
]