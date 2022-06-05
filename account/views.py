from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import render
from . import serializers
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from .tasks import send_activation_code, send_reset_pass
from .permissions import IsSelfUser, IsNotSelfUser
from rest_framework import generics
from .models import Follower
User = get_user_model()


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                # send_confirmation_email(user)  # - just sending without parraleles
                send_activation_code.delay(user.email, user.activation_code)
            return Response('check ur email', status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ActivationView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response('it is activated now', status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'msg': 'Link expired'}, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(TokenObtainPairView):
    serializer_class = serializers.LoginSerializer


class NewPasswordView(APIView):
    def post(self, request):
        serializer = serializers.CreateNewPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response('ur password have been changed')


class ResetPasswordView(APIView):

    def post(self, request):
        serializer = serializers.PasswordResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(email=serializer.data.get('email'))
            user.create_activation_code()
            user.save()
            send_reset_pass.delay(user.activation_code, user.email)
            return Response('check ur email')


class LogoutApiView(GenericAPIView):
    serializer_class = serializers.LogOutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('successfully log out!', status=status.HTTP_204_NO_CONTENT)


class UpdateToAuthorView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsSelfUser, )
    serializer_class = serializers.CreateAuthorSerializer

#
# class CreateFollower(generics.CreateAPIView):
#     queryset = Follower.objects.all()
#     permission_classes = (permissions.IsAuthenticated, IsNotSelfUser,)
#     serializer_class = serializers.FollowerSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(listener=self.request.user)


class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserListViewSerializer


class UserRetrieveView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsSelfUser,)
    serializer_class = serializers.UserViewSerializer


class FollowerViewSet(ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = serializers.FollowerSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated(), ]
        elif self.action in ['create', ]:
            return [IsNotSelfUser(), ]
        else:
            return [IsSelfUser(), ]

    def perform_create(self, serializer):
        serializer.save(listener=self.request.user)


def index(request):
    return render(request, 'paymentpreview.html')
