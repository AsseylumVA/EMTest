# utils/permissions.py

from business.models import BusinessElement
from rbac.models import AccessRoleRule, UserRole


class PermissionChecker:

    def __init__(self, user):
        self.user = user
        self._permissions_cache = {}

    def get_permissions(self, element_code):
        """Получить права пользователя для элемента"""
        if element_code in self._permissions_cache:
            return self._permissions_cache[element_code]

        if not self.user or not self.user.is_authenticated:
            return self._empty_permissions()

        try:
            element = BusinessElement.objects.get(code=element_code)
        except BusinessElement.DoesNotExist:
            return self._empty_permissions()

        # Получаем все правила для ролей пользователя и данного элемента
        rules = AccessRoleRule.objects.filter(
            role__userrole__user=self.user,
            element=element
        ).select_related('role', 'element')

        permissions = self._empty_permissions()
        for rule in rules:
            for perm_name in permissions.keys():
                permissions[perm_name] |= getattr(rule, f"{perm_name}_permission")

        self._permissions_cache[element_code] = permissions
        return permissions

    def has_permission(self, element_code, action, obj=None):
        """Проверить право на элемент"""
        perms = self.get_permissions(element_code)

        # Если есть _all право, доступ разрешен
        if perms.get(f"{action}_all"):
            return True

        if not perms.get(action):
            return False

        if action == 'create' or obj is None:
            return True

        # Иначе проверяем владельца
        owner_id = self._get_owner_id(obj)
        return owner_id == self.user.id if owner_id else False

    def is_admin(self):
        if not self.user or not self.user.is_authenticated:
            return False

        return UserRole.objects.filter(
            user=self.user,
            role__name='admin'
        ).exists()

    @staticmethod
    def _empty_permissions():
        return {
            'read': False,
            'read_all': False,
            'create': False,
            'update': False,
            'update_all': False,
            'delete': False,
            'delete_all': False,
        }

    @staticmethod
    def _get_owner_id(obj):
        if isinstance(obj, dict):
            owner = obj.get('owner')
            return owner.get('id') if isinstance(owner, dict) else owner

        if hasattr(obj, 'owner_id'):
            return obj.owner_id

        if hasattr(obj, 'owner'):
            owner = obj.owner
            return owner.id if hasattr(owner, 'id') else owner

        return None
