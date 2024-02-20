from django.urls import path

from apps.auth_app.api.views import views
from apps.auth_app.api.views import oauth2

urlpatterns = [
    path('register/', views.RegisterViews.as_view()),
    path('login/', views.LoginView.as_view()),
    path('profile/', views.ProfileViews.as_view()),
    path('google/', oauth2.GoogleSocialAuthView.as_view()),
]