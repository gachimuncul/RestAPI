from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from .models import PermissionRule


class CustomAccessPermission(BasePermission):
    def has_permission(self, request, view):
        # Проверяем, что пользователь вообще авторизован (передал валидный токен)
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated(detail="Требуется авторизация (отсутствует или недействителен токен).")

        # Смотрим, какой ресурс защищает данная View
        required_resource = getattr(view, 'required_resource', None)

        # Если View не указала ресурс, значит она открыта для всех залогиненных (например, профиль)
        if not required_resource:
            return True

        # Определяем действие на основе HTTP-метода
        method_to_action = {
            'GET': 'read',
            'POST': 'create',
            'PUT': 'update',
            'PATCH': 'update',
            'DELETE': 'delete'
        }
        required_action = method_to_action.get(request.method)

        # ищем правило в базе данных
        # Логика: есть ли правило, где ресурс = required_resource, действие = required_action,
        # и роль из этого правила назначена текущему пользователю?
        has_access = PermissionRule.objects.filter(
            role__userrole__user=request.user,
            resource__name=required_resource,
            action__name=required_action
        ).exists()

        # Если совпадений нет - выбрасываем 403 Forbidden
        if not has_access:
            raise PermissionDenied(
                detail=f"У вас нет прав на действие '{required_action}' с ресурсом '{required_resource}'.")

        return True