from django.urls import path
from posts import views

urlpatterns = [
    path('', views.posts_list),
    path('<int:pk>/', views.posts_detail),
]