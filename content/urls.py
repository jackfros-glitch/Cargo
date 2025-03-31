from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.create_content, name='create_content'),
    path('', views.get_contents, name='get_contents'),
    path('<int:content_id>/', views.get_content_by_id, name='get_content_by_id'),
    path('<int:content_id>/update/', views.update_content, name='update_content'),
    path('<int:content_id>/delete/', views.delete_content, name='delete_content'),
]
