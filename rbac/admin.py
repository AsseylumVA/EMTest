from django.contrib import admin

from .models import AccessRoleRule, Role, UserRole


class AccessRoleRuleInline(admin.TabularInline):
    model = AccessRoleRule
    extra = 1
    fields = ('element', 'read_permission', 'read_all_permission', 'create_permission',
              'update_permission', 'update_all_permission', 'delete_permission',
              'delete_all_permission')
    verbose_name = "Правило доступа"
    verbose_name_plural = "Правила доступа"


class UserRoleInline(admin.TabularInline):
    model = UserRole
    extra = 1
    verbose_name = "Пользователь с ролью"
    verbose_name_plural = "Пользователи с ролью"


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_count', 'rule_count')
    search_fields = ('name',)
    inlines = [UserRoleInline, AccessRoleRuleInline]

    def user_count(self, obj):
        return obj.userrole_set.count()

    user_count.short_description = 'Пользователей'

    def rule_count(self, obj):
        return obj.accessrolerule_set.count()

    rule_count.short_description = 'Правил'


@admin.register(AccessRoleRule)
class AccessRoleRuleAdmin(admin.ModelAdmin):
    pass
