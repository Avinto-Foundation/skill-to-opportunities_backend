"""Role-based permission classes.

Use them on views, for example ``permission_classes = [IsEmployer]``.
"""
from rest_framework.permissions import BasePermission

from .models import Role


class _HasRole(BasePermission):
    role: str = ""

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.role == self.role)


class IsCandidate(_HasRole):
    role = Role.CANDIDATE


class IsEmployer(_HasRole):
    role = Role.EMPLOYER


class IsAdminRole(_HasRole):
    role = Role.ADMIN
