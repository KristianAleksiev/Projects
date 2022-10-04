from ToDoWorkshop.todo_auth.serializers import CreateUserSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

UserModel = get_user_model()


#  Register
class RegisterView(generics.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny,)


# Token authentication, settings setup, local storage
class LoginView(ObtainAuthToken):
    permission_classes = (permissions.AllowAny,)


#  Logging out
class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def __perform_logout(request):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({"message": "User logged out!"})

    def get(self, request):
        return self.__perform_logout(request)

    def post(self, request):
        return self.__perform_logout(request)
