from django.urls import path
from . import views as manager_views

urlpatterns = [
    path('', manager_views.home, name='home'),
    path('new/acc/', manager_views.create_account, name='create-account'),
    path('<str:pk>/new/char/', manager_views.create_char, name='create-char'),
    path('update_date/<str:name>/', manager_views.update_date, name='update-date'),
    path('delete/char/<int:pk>', manager_views.CharacterDeleteView.as_view(), name='delete-char'),
    path('delete/acc/<int:pk>', manager_views.AccountDeleteView.as_view(), name='delete-acc'),
    path('delete/', manager_views.delete_char, name='delete_char')
]
