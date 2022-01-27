from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from DoNotExpire.profiles import views as profiles_views

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='profiles/login.html',
        redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(template_name='profiles/logout.html'), name='logout'),
    path('register/', profiles_views.register, name='register'),
    path('profile/', profiles_views.profile, name='profile')
]
