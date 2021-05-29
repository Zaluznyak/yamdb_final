from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdmin
from .serializers import UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def RegisterView(request):
    """Регистрация пользователя по email и генерация кода."""
    email = request.data.get('email')
    username = email[:email.find('@')]
    user = User.objects.get_or_create(email=email, username=username)[0]
    confirm_code = default_token_generator.make_token(user)
    serializer = UserSerializer(
        user, data={'confirmation_code': confirm_code}, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    send_mail('Регистрация на YaMDB', f'Ваш код: {confirm_code}',
              settings.FROM_EMAIL, [email], fail_silently=False)
    return Response({'email': email})


@api_view(['POST'])
@permission_classes([AllowAny])
def TokenView(request):
    """Получения токена по email и коду доступа."""
    def get_token(user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    email = request.data.get('email')
    confirm_code = request.data.get('confirmation_code')
    user = get_object_or_404(User, email=email)
    if user.confirmation_code == confirm_code:
        response = {'token': get_token(user)}
        return Response(response, status=status.HTTP_200_OK)
    response = {'confirmation_code': 'Неверный код для данного email'}
    return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        """Получение и редактирования своих данных"""
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
