from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from business.models import BusinessElement
from rbac.permissions import IsAdmin
from rbac.serializers import (AccessRoleRuleSerializer, AssignRoleSerializer,
                              BusinessElementSerializer, RoleSerializer,
                              UserRoleSerializer)
from rbac.models import AccessRoleRule, Role, UserRole


class AdminViewSetMixin:
    permission_classes = [IsAdmin]


class RoleViewSet(AdminViewSetMixin, viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class BusinessElementViewSet(AdminViewSetMixin, viewsets.ModelViewSet):
    queryset = BusinessElement.objects.all()
    serializer_class = BusinessElementSerializer


class AccessRoleRuleViewSet(AdminViewSetMixin, viewsets.ModelViewSet):
    queryset = AccessRoleRule.objects.select_related('role', 'element').all()
    serializer_class = AccessRoleRuleSerializer
    filterset_fields = ['role', 'element']


class UserRoleViewSet(AdminViewSetMixin, viewsets.ModelViewSet):
    queryset = UserRole.objects.select_related('user', 'role').all()
    serializer_class = UserRoleSerializer
    filterset_fields = ['user', 'role']

    @action(detail=False, methods=['POST'], serializer_class=AssignRoleSerializer)
    def assign(self, request):
        """
        Назначить роль пользователю по email.
        POST /rbac/user-roles/assign/
        {"email": "user@example.com", "role_id": 1}
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_role = serializer.save()

        return Response(
            UserRoleSerializer(user_role).data,
            status=status.HTTP_201_CREATED
        )
