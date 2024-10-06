# webapp/auth/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/view/<int:user_id>/', views.another_profile, name='another_profile'),
    path('profile/', views.profile, name='profile'),
    path('profile/update', views.profile_update, name='profile_update'),
    path('profile/page/post', views.create_post, name='profile_create_post'),
    path('profile/<path:page>', views.profile, name='profile_page'),
    path('profile/<int:user_id>/<path:page>/', views.profile, name='profile_id_page'),
    path('profile/social/update', views.activation_social_profile, name='activation_social_profile'),
]