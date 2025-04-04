from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import register_user, LoginView, track_user_activity

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('activities/', track_user_activity, name='track_user_activity'),    
]
