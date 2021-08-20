from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views as api_views
from .views import AccountViewSet, CharacterViewSet

router = DefaultRouter()
router.register(r'accs', AccountViewSet, basename='accs')
router.register(r'chars', CharacterViewSet, basename='chars')

urlpatterns = [
    *router.urls,
    path('chars/<str:charname>/equipment', api_views.CharacterEquipmentView.as_view(), name='char_eq'),
    path('chars/<str:charname>/bump', api_views.CharacterBumpLastVisited.as_view(), name='char-bump-last-visited'),
]
