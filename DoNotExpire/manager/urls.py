from django.urls import path
from . import views as manager_views

urlpatterns = [
    path('', manager_views.home, name='home'),
    path('newacc/', manager_views.create_account, name='create_account'),
    path('newchar/', manager_views.create_char, name='create_char'),
]
