from django.urls import path
from . import views as manager_views

urlpatterns = [
    path('', manager_views.home, name='home'),
    path('newacc/', manager_views.create_account, name='create-account'),
    path('newchar/', manager_views.create_char, name='create-char'),
    path('update_date/<str:name>/', manager_views.update_date, name='update-date'),
    path('delete/', manager_views.delete_char, name='delete-char'),
]
