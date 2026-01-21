from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from rbac.permissions import HasElementPermission
from utils.permissions import PermissionChecker


class MockViewSet(ViewSet):
    permission_classes = [HasElementPermission]
    element_code = None

    def get_mock_data(self):
        return []

    def _filter_by_owner(self, data):
        checker = PermissionChecker(self.request.user)
        perms = checker.get_permissions(self.element_code)

        if perms['read_all']:
            return data

        return [
            item for item in data
            if item.get('owner', {}).get('id') == self.request.user.id
        ]

    def _get_object_or_404(self, pk):
        try:
            all_data = self.get_mock_data()
            return next(item for item in all_data if item['id'] == int(pk))
        except (StopIteration, ValueError):
            return None

    def list(self, request):
        data = self._filter_by_owner(self.get_mock_data())
        return Response(data)

    def retrieve(self, request, pk=None):
        obj = self._get_object_or_404(pk)
        if not obj:
            return Response(
                {'detail': 'Not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        checker = PermissionChecker(request.user)
        if not checker.has_permission(self.element_code, 'read', obj):
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response(obj)

    def create(self, request):
        new_obj = {
            'id': 999,
            'owner': {
                'id': request.user.id,
                'email': request.user.email
            },
            **request.data
        }
        return Response(new_obj, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        obj = self._get_object_or_404(pk)
        if not obj:
            return Response(
                {'detail': 'Not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        checker = PermissionChecker(request.user)
        if not checker.has_permission(self.element_code, 'update', obj):
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )

        updated_obj = {**obj, **request.data}
        return Response(updated_obj)

    def partial_update(self, request, pk=None):
        obj = self._get_object_or_404(pk)
        if not obj:
            return Response(
                {'detail': 'Not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        checker = PermissionChecker(request.user)
        if not checker.has_permission(self.element_code, 'update', obj):
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )

        updated_obj = {**obj, **request.data}
        return Response(updated_obj)

    def destroy(self, request, pk=None):
        obj = self._get_object_or_404(pk)
        if not obj:
            return Response(
                {'detail': 'Not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        checker = PermissionChecker(request.user)
        if not checker.has_permission(self.element_code, 'delete', obj):
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(MockViewSet):
    element_code = 'products'

    def get_mock_data(self):
        return [
            {
                'id': 1,
                'name': 'Laptop',
                'price': 1200,
                'owner': {'id': 1, 'email': 'admin@example.com'}
            },
            {
                'id': 2,
                'name': 'Mouse',
                'price': 25,
                'owner': {'id': 2, 'email': 'user@example.com'}
            },
            {
                'id': 3,
                'name': 'Keyboard',
                'price': 75,
                'owner': {'id': 1, 'email': 'admin@example.com'}
            },
        ]


class OrderViewSet(MockViewSet):
    element_code = 'orders'

    def get_mock_data(self):
        return [
            {
                'id': 1,
                'items': [
                    {'product': 'Laptop', 'quantity': 1, 'price': 1200},
                    {'product': 'Mouse', 'quantity': 2, 'price': 25},
                ],
                'total': 1250,
                'owner': {'id': 2, 'email': 'user@example.com'}
            },
            {
                'id': 2,
                'items': [
                    {'product': 'Keyboard', 'quantity': 1, 'price': 75},
                    {'product': 'Monitor', 'quantity': 1, 'price': 300},
                ],
                'total': 375,
                'owner': {'id': 1, 'email': 'admin@example.com'}
            },
            {
                'id': 3,
                'items': [
                    {'product': 'Mouse', 'quantity': 5, 'price': 25},
                ],
                'total': 125,
                'owner': {'id': 2, 'email': 'user@example.com'}
            },
        ]


class StoreViewSet(MockViewSet):
    element_code = 'stores'

    def get_mock_data(self):
        return [
            {
                'id': 1,
                'name': 'Main Store',
                'address': '123 Main St',
                'owner': {'id': 1, 'email': 'admin@example.com'}
            },
            {
                'id': 2,
                'name': 'Branch Store',
                'address': '456 Oak Ave',
                'owner': {'id': 1, 'email': 'admin@example.com'}
            },
        ]
