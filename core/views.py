from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from django.contrib.auth import get_user_model
from .permissions import CustomAccessPermission


User = get_user_model()


# Регистрация
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer


# Профиль (Получение, Обновление, Удаление)
class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()

        # Логаут: помещаем текущий refresh токен в черный список (если он передан)
        refresh_token = request.data.get("refresh")
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass

        return Response({"detail": "Аккаунт удален, выполнен выход."}, status=status.HTTP_204_NO_CONTENT)


# Принудительный Логаут
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Успешный выход из системы."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"detail": "Неверный или отсутствующий токен."}, status=status.HTTP_400_BAD_REQUEST)


class MockFinancialReportView(APIView):
    permission_classes = [CustomAccessPermission]
    required_resource = 'financial_reports'

    def get(self, request):
        # Если код дошел сюда, значит разрешение получено возвращаем фейковые данные.
        mock_data = [
            {"id": 1, "month": "Январь", "revenue": 500000},
            {"id": 2, "month": "Февраль", "revenue": 650000}
        ]
        return Response({"message": "Доступ разрешен!", "data": mock_data})

    def post(self, request):
        return Response({"message": "Отчет успешно создан!"}, status=status.HTTP_201_CREATED)