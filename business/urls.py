from rest_framework.routers import DefaultRouter

from business.views import OrderViewSet, ProductViewSet, StoreViewSet

app_name = 'business'
router = DefaultRouter()

router.register('products', ProductViewSet, basename='products')
router.register('orders', OrderViewSet, basename='orders')
router.register('stores', StoreViewSet, basename='stores')

urlpatterns = router.urls
