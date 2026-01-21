from rest_framework.routers import DefaultRouter

from rbac.views import (AccessRoleRuleViewSet, BusinessElementViewSet, RoleViewSet,
                        UserRoleViewSet)

app_name = 'rbac'
router = DefaultRouter()

router.register('roles', RoleViewSet, basename='roles')
router.register('elements', BusinessElementViewSet, basename='elements')
router.register('rules', AccessRoleRuleViewSet, basename='rules')
router.register('user-roles', UserRoleViewSet, basename='user-roles')

urlpatterns = router.urls
