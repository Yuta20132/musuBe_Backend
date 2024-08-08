from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import CustomUser
from .serializers import UserSerializer
from django.conf import settings
from rest_framework.views import APIView
from .serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken

###ユーザーに関するView
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    #ユーザー登録の関数
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # デバッグ用にエラーをログに出力
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()

        activation_url = reverse('activate', args=[user.pk])
        full_url = f"{settings.FRONTEND_URL}/activate/{user.id}/"
        send_mail(
            'Activate your account',
            f'Please click the following link to activate your account: {full_url}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )

        return Response({'message': 'User registered successfully. Please check your email to activate your account.'}, status=status.HTTP_201_CREATED)
    
    #ユーザーを削除する関数（開発用）
    @action(detail=False, methods=['delete'])
    def delete_user(self, request):
        username = request.data.get('username')
        if not username:
            return Response({'error':'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(CustomUser, username=username)
        user.delete()
        return Response({'message':'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    

###ユーザー登録時のアクティベート化
def activate(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if user.is_active:
        return JsonResponse({'message': 'Your account has already been activated.'})
    user.is_active = True
    user.save()
    return JsonResponse({'message': 'Your account has been activated successfully.'})

###ユーザーログインのView
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)