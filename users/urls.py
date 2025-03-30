from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import register_user, LoginView

urlpatterns = [
    path('api/users/register/', register_user, name='register_user'),
    path('api/users/login/', LoginView.as_view(), name='token_obtain_pair'),
    path('api/users/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    
]
