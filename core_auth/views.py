from rest_framework import status, permissions
from .serializers import RegisterSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import APIView 
from django.contrib.auth import authenticate
from rest_framework.authtoken.serializers import AuthTokenSerializer
# from rest_framework_api_key.models import APIKey
from ip_locator.models import APIKEYMOD, Userprofile
from ip_locator.serializers import APIKeySerializer
import uuid




class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request: Request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            userr = serializer.save()
            userprofile = Userprofile.objects.create(user=userr)
            my_api_key = uuid.uuid4()
            api_keys = APIKEYMOD(api_key=my_api_key,user=userprofile)
            api_keys.save()
            api_serializer = APIKeySerializer(instance=api_keys)


            response = {
                "MESSAGE": "User Created Successfully", 
                "REGISTERED_USER": serializer.data,
                "API_SERIALIZER": api_serializer.data,
                #'token' : token.key
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):

    def post(self, request: Request):
        serializer = AuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username = username, password = password)
            token, created = Token.objects.get_or_create(user=user)

            response = {
                "MESSAGE": "Login Successfull", 
                "TOKEN": token.key
            }

            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(data={"message": "Invalid email or password"})


    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}

        return Response(data=content, status=status.HTTP_200_OK)



class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, format=None):
        request.user.auth_token.delete()
        return Response({"MESSAGE": "You are logged out"}, status=status.HTTP_200_OK)