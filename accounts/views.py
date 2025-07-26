from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserLoginSerializer, UserRegistrationSerializer
from django.contrib.auth import get_user_model
#from projectmitra.utils.email_utils import send_custom_email

# Inside RegisterAPIView
User = get_user_model()

#Admin Account Creation
class CreateAdminUserView(APIView):
    def post(self, request):
        email = 'arkodip4@example.com'  # Change if needed
        password = 'password123'        # Use strong password

        if not User.objects.filter(email=email).exists():
            admin = User.objects.create_superuser(
                email=email,
                name='Arkodip Admin',
                password=password,
                role='admin',
                is_staff=True,
                is_superuser=True
            )

            refresh = RefreshToken.for_user(admin)

            return Response({
                "message": "Admin user created successfully.",
                "admin": {
                    "id": admin.id,
                    "email": admin.email,
                    "name": admin.name,
                    "role": admin.role
                },
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        else:
            # Generate token for existing admin
            admin = User.objects.get(email=email)
            refresh = RefreshToken.for_user(admin)

            return Response({
                "message": "Admin user already exists.",
                "admin": {
                    "id": admin.id,
                    "email": admin.email,
                    "name": admin.name,
                    "role": admin.role
                },
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)



class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User registered successfully",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role
                }
            }, status=status.HTTP_201_CREATED)
        """send_custom_email(  # for email notification
        subject="Welcome to ProjectMitra!",
        message=f"Hi {user.name}, your registration was successful. You can now start using ProjectMitra.",
        recipient_list=[user.email]
        )   """ 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=200)
        except Exception as e:
            return Response({"error": "Logout failed", "details": str(e)}, status=400)