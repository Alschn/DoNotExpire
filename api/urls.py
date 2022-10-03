from rest_framework.routers import DefaultRouter

from .views.accounts import AccountsViewSet
from .views.characters import CharactersViewSet

router = DefaultRouter()
router.register(r'accounts', AccountsViewSet, basename='accounts')
router.register(r'characters', CharactersViewSet, basename='characters')

urlpatterns = router.urls
