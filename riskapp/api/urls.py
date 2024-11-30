from django.urls import path

from riskapp.api.views import (
    ProjectRiskListApiView
)
app_name = 'riskapp_api'

urlpatterns = [
    path("project_risks/<int:project_id>", ProjectRiskListApiView.as_view())
]