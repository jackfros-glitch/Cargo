from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.create_subscription, name = 'create_user_sub'),
    path('', views.get_all_subscriptions, name="subscription_list"), 
    path('<int:sub_id>', views.get_subscription_by_id, name="subscription_by_id"), 
    path("renew/<int:sub_id>", views.renew_subscription, name="renew_subscription"),
    path("delete/<int:sub_id>", views.delete_subscription, name="delete_subscription"),      
]
