from rest_framework.routers import DefaultRouter

from users.views import AuthViewSet, ProfileViewSet

app_name = 'users'
router = DefaultRouter()

router.register('', ProfileViewSet, basename='profile')
router.register('auth', AuthViewSet, basename='auth')

urlpatterns = router.urls
