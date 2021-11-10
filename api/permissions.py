from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

User = get_user_model()


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff


class ReviewCommentPermissions(BasePermission):
    """Права доступа для комментариев и отзывов"""
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return request.user.is_authenticated()
        return ((request.method in SAFE_METHODS)
                or request.user == obj.author
                or request.user.is_admin
                or request.user.is_moderator)
