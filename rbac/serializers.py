from django.contrib.auth import get_user_model
from rest_framework import serializers

from business.models import BusinessElement
from rbac.models import AccessRoleRule, Role, UserRole

User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name')


class BusinessElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessElement
        fields = ('id', 'code', 'description')


class AccessRoleRuleSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    element_code = serializers.CharField(source='element.code', read_only=True)

    class Meta:
        model = AccessRoleRule
        fields = (
            'id', 'role', 'role_name', 'element', 'element_code',
            'read_permission', 'read_all_permission',
            'create_permission',
            'update_permission', 'update_all_permission',
            'delete_permission', 'delete_all_permission'
        )


class UserRoleSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    role_name = serializers.CharField(source='role.name', read_only=True)

    class Meta:
        model = UserRole
        fields = ('id', 'user', 'user_email', 'role', 'role_name')

    def validate(self, data):
        user = data.get('user')
        role = data.get('role')

        if UserRole.objects.filter(user=user, role=role).exists():
            raise serializers.ValidationError(
                'This user already has this role.'
            )

        return data


class AssignRoleSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role_id = serializers.IntegerField()

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist.')
        return value

    def validate_role_id(self, value):
        try:
            Role.objects.get(id=value)
        except Role.DoesNotExist:
            raise serializers.ValidationError('Role does not exist.')
        return value

    def validate(self, data):
        user = User.objects.get(email=data['email'])
        role = Role.objects.get(id=data['role_id'])

        if UserRole.objects.filter(user=user, role=role).exists():
            raise serializers.ValidationError(
                'This user already has this role.'
            )

        data['user'] = user
        data['role'] = role
        return data

    def create(self, validated_data):
        return UserRole.objects.create(
            user=validated_data['user'],
            role=validated_data['role']
        )
