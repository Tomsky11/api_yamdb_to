from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    ReviewsViewSet,
    CommentViewSet,
    UserViewSet,
    TitlesViewSet,
    CategoriesViewSet,
    GenresViewSet,
    get_token,
    send_confirmation_code
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


router_v1 = DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='api_reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='api_comments'
)
router_v1.register('titles', TitlesViewSet, basename='titles')
router_v1.register('users', UserViewSet)
router_v1.register('categories', CategoriesViewSet, basename='categories')
router_v1.register('genres', GenresViewSet, basename='genres')


v1_auth_patterns = [
    path('email/', send_confirmation_code),
    path('token/', get_token),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = [
    path('v1/auth/', include(v1_auth_patterns)),
    path('v1/', include(router_v1.urls)),
]
