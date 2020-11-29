from django.urls import path

from . import views

urlpatterns = [
    path('vk/', views.VkApiView.as_view()),
    path('vk/<int:vk_user_id>/', views.VkApiView.as_view()),
    path('vk/image/', views.VkImageApiView.as_view())
]
