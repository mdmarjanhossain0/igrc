from django.urls import path

from account.api.views import (
    Login,
    send_otp_view,
    register_view,
    AccountListApiView,
    TenantAccountListApiView
)
app_name = 'account_api'

urlpatterns = [
    path("login", Login.as_view()),
    path("send_otp/<mobile>", send_otp_view),
    path("register", register_view),
    path("user_list", AccountListApiView.as_view()),
    path("tenant_user_list/<int:tenant_id>", TenantAccountListApiView.as_view())
]