from django_filters.rest_framework import DjangoFilterBackend
from .utils import generate_mail
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.contrib.auth.tokens import default_token_generator
from .filters import TitleFilter
from rest_framework.response import Response
from rest_framework import mixins, viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action, api_view, permission_classes
from .permissions import (
    IsAdmin, IsAdminUserOrReadOnly, ReviewCommentPermissions
)
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from .models import Titles, Reviews, Titles, Categories, Genres
from .serializers import (
    CommentSerializer,
    ReviewsSerializer,
    GenresSerializer,
    TitlesReadSerializer,
    CategoriesSerializer,
    TitlesCreateSerializer,
    UserSerializer,
    EmailAuthSerializer,
    UserEmailSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from .utils import generate_mail
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser | IsAdmin]
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = [SearchFilter]
    search_fields = ['username', ]

    @action(methods=['patch', 'get'], detail=False,
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role, partial=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_confirmation_code(request):
    serializer = UserEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data['email']
    user = get_object_or_404(User, email=email)
    confirmation_code = default_token_generator.make_token(user)
    generate_mail(email, confirmation_code)
    return Response(
        {'Успешно': 'На вашу почту был выслан код подтверждения'}
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    email = request.data['email']
    confirmation_code = request.data['confirmation_code']
    user = get_object_or_404(User, email=email)
    if default_token_generator.check_token(user, confirmation_code):
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })
    return Response(request.data, status=status.HTTP_400_BAD_REQUEST)


class UserRegToken(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailAuthSerializer(date=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = AccessToken.for_user(user=user)
        return Response({'token': str(token)})


class ModelMixinSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Класс для дальнейшего наследования."""

    pass


class CategoriesViewSet(ModelMixinSet):
    pagination_class = PageNumberPagination
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['name', ]
    permission_classes = [IsAdminUserOrReadOnly]


class GenresViewSet(ModelMixinSet):
    pagination_class = PageNumberPagination
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['name', ]
    permission_classes = [IsAdminUserOrReadOnly]


class TitlesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = Titles.objects.all().annotate(Avg('reviews_title__score'))
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    filterset_fields = ['name', 'category', 'genre', 'year']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesReadSerializer
        return TitlesCreateSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    permission_classes = [ReviewCommentPermissions, IsAuthenticatedOrReadOnly]
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        queryset = Reviews.objects.filter(
            title__id=self.kwargs.get('title_id')
        )
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    permission_classes = [ReviewCommentPermissions, IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Reviews, pk=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Reviews,
            pk=self.kwargs['review_id'],
            title__id=self.kwargs['title_id']
        )
        serializer.save(author=self.request.user, review=review)
