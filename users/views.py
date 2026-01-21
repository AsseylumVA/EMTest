from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.serializers import ChangePasswordSerializer, LoginSerializer, \
    ProfileSerializer, RegisterSerializer
from utils.jwt_utils import create_jwt

User = get_user_model()


class ProfileViewSet(GenericViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @action(detail=False, methods=['GET'])
    def me(self, request):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    @action(detail=False, methods=['PUT'])
    def update_profile(self, request):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(detail=False, methods=['PATCH'])
    def partial_update_profile(self, request):
        user = self.get_object()

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(detail=False, methods=['DELETE'])
    def deactivate(self, request):
        user = self.get_object()
        user.is_active = False
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['POST'], serializer_class=ChangePasswordSerializer)
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.get_object()
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({'detail': 'Password updated successfully.'})


class AuthViewSet(GenericViewSet):

    @action(detail=False, methods=['POST', ], serializer_class=RegisterSerializer,
            permission_classes=[AllowAny])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ProfileSerializer(serializer.instance).data,
                        status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST', ], serializer_class=LoginSerializer,
            permission_classes=[AllowAny])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token = create_jwt(user.id)

        return Response({'access': token}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST', ], permission_classes=[IsAuthenticated])
    def logout(self, request):
        return Response({'detail': 'Logged out'}, status=status.HTTP_200_OK)
