from .serializers import UserSerializer, TokenSerializer, SingUpSerializer, MeSerializer, UserListSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import default_token_generator
from reviews.models import User
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import mixins
from django.shortcuts import get_list_or_404, get_object_or_404


def sent_verification_code(user):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения',
        f'Ваш код: {confirmation_code}',
        'db_yamdb@example.com',
        [user.email],
        fail_silently=False,
    )


# Доступно всем
class SignUp(APIView):
    permission_classes = [AllowAny]
    serializer_class = SingUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not User.objects.filter(username=request.user.username).exists():
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user = serializer.instance
            sent_verification_code(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        elif User.objects.filter(username=request.user.username).exists():
            user = get_object_or_404(User, username=request.data['username'])
            sent_verification_code(user)
            return Response(request.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def get_token(request):

    if User.objects.filter(username=request.data['username']).exists():
        user = get_object_or_404(User, username=request.data['username'])
        if default_token_generator.check_token(user, request.data['confirmation_code']):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response('Отсутствует обязательное поле или оно некорректно', status=status.HTTP_400_BAD_REQUEST)
    return Response('Пользователь не найден', status=status.HTTP_404_NOT_FOUND)



# Доступно только админу(GET POST PATCH DELETE)
class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = "username"




class UpdateListViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pass


# Доступно любому авторизированному user
@api_view(['GET', 'PATCH'])
def get_update_me(request):
    if request.method == "PATCH":
        me = get_object_or_404(User, username=request.user.username)
        serializer = MeSerializer(me, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    me = get_object_or_404(User, username=request.user.username)
    serializer = MeSerializer(me)
    return Response(serializer.data)
