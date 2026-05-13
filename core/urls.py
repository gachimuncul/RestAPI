from django.urls import path, include  # добавили include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, UserProfileView, LogoutView, MockFinancialReportView,
    RoleViewSet, ResourceViewSet, ActionViewSet, PermissionRuleViewSet, UserRoleViewSet
)

# Создаем роутер и регистрируем наши админские пути
router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='roles')
router.register(r'resources', ResourceViewSet, basename='resources')
router.register(r'actions', ActionViewSet, basename='actions')
router.register(r'rules', PermissionRuleViewSet, basename='rules')
router.register(r'user-roles', UserRoleViewSet, basename='user-roles')

urlpatterns = [
    # Пути авторизации
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),

    # Защищенный бизнес-ресурс
    path('reports/', MockFinancialReportView.as_view(), name='reports'),

    # Подключаем все админские пути одним разом по префиксу /admin-api/
    path('admin-api/', include(router.urls)),
]