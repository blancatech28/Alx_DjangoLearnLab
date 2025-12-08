from django.urls import path
from .views import RegisterView, LoginView, ProfileView
from .views import DevelopView

develop_view = DevelopView.as_view()

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'), 
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', develop_view, name='follow-user'),
    path('unfollow/<int:user_id>/', develop_view, name='unfollow-user'),
]
