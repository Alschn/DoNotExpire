from django.urls import path

from profiles import views as profiles_views

urlpatterns = [
    path('login/', profiles_views.LoginView.as_view(), name='login'),
    path('logout/', profiles_views.LogoutView.as_view(), name='logout'),
    path('register/', profiles_views.register, name='register'),
    path('profile/', profiles_views.profile, name='profile')
]
