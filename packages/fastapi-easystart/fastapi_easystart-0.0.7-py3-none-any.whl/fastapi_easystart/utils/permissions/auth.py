from fastapi import Request


class BasePermission:
    def has_permission(self, request: Request) -> bool:
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True


class AllowAny(BasePermission):
    def has_permission(self, request: Request) -> bool:
        return True


class IsAuthenticated(BasePermission):
    def has_permission(self, request: Request) -> bool:
        user = getattr(request.state, "user", None)
        return user is not None and user.is_authenticated


class IsAdminUser(BasePermission):
    def has_permission(self, request: Request) -> bool:
        user = getattr(request.state, "user", None)
        return user is not None and user.is_staff


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request: Request) -> bool:
        user = getattr(request.state, "user", None)
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return user is not None and user.is_authenticated
