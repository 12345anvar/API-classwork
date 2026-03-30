from django.urls import path
from posts import views
from posts.views import RegisterView

urlpatterns = [
    path('', views.posts_list),
    path('<int:pk>/', views.posts_detail),
    path('register/', RegisterView.as_view(), name='register')
]