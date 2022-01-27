from django.urls import path
from . import views as manager_views

urlpatterns = [
    path('', manager_views.home, name='home'),
    path('new/acc/', manager_views.create_account, name='create-account'),
    path('<str:acc_name>/new/char/', manager_views.create_char, name='create-char'),
    path('delete/acc/<int:pk>', manager_views.AccountDeleteView.as_view(), name='delete-acc'),
]
