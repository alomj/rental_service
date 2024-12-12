import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .forms import UserEditProfileForm

User = get_user_model()
from .serializer import UserRegistrationSerializer


@login_required
def home_view(request):
    return render(request, 'user/index.html')


@login_required
def profile(request):
    return render(request, 'user/profile.html')


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = UserEditProfileForm(instance=request.user)
        return render(request, 'user/edit_profile.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserEditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, 'user/edit_profile.html', {'form': form})


def register(request):
    errors = []
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        try:
            response = requests.post(
                'http://127.0.0.1:8000/register_api/',
                data={
                    'username': username,
                    'email': email,
                    'password': password,
                    'password_confirm': confirm_password,
                },
                headers={'X-CSRFToken': request.COOKIES.get('csrftoken')}
            )
            print("Response Status Code:", response.status_code)
            print("Response Content:", response.text)

            if response.status_code == 201:
                return render(request, 'user/register_success.html')
            else:
                try:
                    error_data = response.json()
                    errors.extend([f"{field}: {' '.join(messages)}" for field, messages in error_data.items()])
                except ValueError:
                    errors.append(f"Unexpected response format: {response.text}")

        except requests.exceptions.RequestException as e:
            errors.append(f"Request error: {str(e)}")

    return render(request, 'user/register.html', {'errors': errors})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                next_url = request.GET.get('next', '/home/')

                response = redirect(next_url)
                response.set_cookie(
                    key='access_token',
                    value=access_token,
                    httponly=True,
                    secure=True,
                    samesite='None',
                    path='/'
                )
                response.set_cookie(
                    key='refresh_token',
                    value=refresh_token,
                    httponly=True,
                    secure=True,
                    samesite='None',
                    path='/'
                )
                return response
            else:
                return render(request, 'user/login.html', {'errors': 'Wrong Login or Password'})
        except User.DoesNotExist:
            return render(request, 'user/login.html', {'errors': 'User doesn`t exist'})

    return render(request, 'user/login.html')


def logout_redirect_view(request):
    logout(request)
    return redirect('login')


class CustomTokenObtainView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)

            # Отримуємо токени
            if response.status_code == 200:
                token = response.data
                access_token = token.get('access')
                refresh_token = token.get('refresh')

                res = redirect(request.GET.get('next', '/home/'))
                res.set_cookie(
                    key='access_token',
                    value=access_token,
                    httponly=True,
                    secure=True,
                    samesite='None',
                    path='/'
                )
                res.set_cookie(
                    key='refresh_token',
                    value=refresh_token,
                    httponly=True,
                    secure=True,
                    samesite='None',
                    path='/'
                )
                return res

            return Response({'success': False}, status=response.status_code)
        except Exception as e:
            print(e)
            return Response({'success': False, 'error': str(e)}, status=400)


class CustomRefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')

            request.data['refresh'] = refresh_token
            response = super().post(request, *args, **kwargs)

            tokens = response.data
            access_token = tokens['access']

            res = Response()

            res.data = {'refreshed': True}

            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'

            )
            return res
        except Exception as e:
            print(e)
            return Response({'refreshed': False}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()

        res = Response({'message': 'Logged out successfully'}, status=200)
        res.delete_cookie('access_token')
        res.delete_cookie('refresh_token')

        return res
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def is_authenticated(request):
    return Response({'authenticated': True})


@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    print("Received request:", request.data)
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
