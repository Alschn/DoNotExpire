from django.urls import path
from . import views as api_views

urlpatterns = [
    path('chars/<str:charname>', api_views.GetEquipment.as_view(), name='char_eq'),
    path('equipments/<str:charname>', api_views.UpdateEquipment.as_view(), name='eq_update')
]
