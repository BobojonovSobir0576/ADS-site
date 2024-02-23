from django.urls import path
from apps.ads.api.views import job_views

urlpatterns = [
    path('', job_views.JobListView.as_view())
]