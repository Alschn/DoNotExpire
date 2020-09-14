from django.urls import path
from . import views as manager_views

urlpatterns = [
    path('', manager_views.home, name='home'),
]
