from django.urls import path

from manager.views import (
    AccountsListView,
    AccountsCreateView,
    AccountDeleteView
)
from manager.views.character_create import CharacterCreateView

urlpatterns = [
    path('', AccountsListView.as_view(), name='home'),
    path('accounts/create', AccountsCreateView.as_view(), name='account-create'),
    path('accounts/<str:name>/characters/create', CharacterCreateView.as_view(),
         name='account-detail-character-create'),
    path('accounts/<int:pk>', AccountDeleteView.as_view(), name='account-detail-delete'),
]
