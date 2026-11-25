"""Tests for every authentication endpoint and the role permissions."""
import pytest
from django.urls import reverse
from rest_framework.test import APIClient, APIRequestFactory

from accounts.models import Role, User
from accounts.permissions import IsAdminRole, IsCandidate, IsEmployer

pytestmark = pytest.mark.django_db

PASSWORD = "Str0ng-Pass-123"


@pytest.fixture
def client():
    return APIClient()


def register(client, **overrides):
    data = {"email": "neha@example.com", "full_name": "Neha", "role": "candidate", "password": PASSWORD}
    data.update(overrides)
    return client.post(reverse("register"), data, format="json")


class TestRegister:
    def test_candidate_can_register(self, client):
        res = register(client)
        assert res.status_code == 201
        assert res.data["email"] == "neha@example.com"
        assert "password" not in res.data
        assert User.objects.get(email="neha@example.com").role == Role.CANDIDATE

    def test_employer_can_register(self, client):
        assert register(client, email="hr@example.com", role="employer").status_code == 201

    def test_cannot_register_as_admin(self, client):
        res = register(client, role="admin")
        assert res.status_code == 400
        assert not User.objects.filter(email="neha@example.com").exists()

    def test_duplicate_email_rejected_case_insensitive(self, client):
        register(client)
        assert register(client, email="NEHA@example.com").status_code == 400

    def test_weak_password_rejected(self, client):
        assert register(client, password="12345678").status_code == 400

    def test_missing_fields_rejected(self, client):
        assert client.post(reverse("register"), {}, format="json").status_code == 400


class TestLogin:
    def test_login_returns_tokens(self, client):
        register(client)
        res = client.post(reverse("login"), {"email": "neha@example.com", "password": PASSWORD}, format="json")
        assert res.status_code == 200
        assert "access" in res.data and "refresh" in res.data

    def test_wrong_password_rejected(self, client):
        register(client)
        res = client.post(reverse("login"), {"email": "neha@example.com", "password": "wrong"}, format="json")
        assert res.status_code == 401

    def test_unknown_user_rejected(self, client):
        res = client.post(reverse("login"), {"email": "x@example.com", "password": PASSWORD}, format="json")
        assert res.status_code == 401


class TestRefresh:
    def test_refresh_gives_new_access_token(self, client):
        register(client)
        tokens = client.post(reverse("login"), {"email": "neha@example.com", "password": PASSWORD}, format="json").data
        res = client.post(reverse("token-refresh"), {"refresh": tokens["refresh"]}, format="json")
        assert res.status_code == 200
        assert "access" in res.data

    def test_invalid_refresh_rejected(self, client):
        assert client.post(reverse("token-refresh"), {"refresh": "nope"}, format="json").status_code == 401


class TestMe:
    def test_requires_authentication(self, client):
        assert client.get(reverse("me")).status_code == 401

    def test_returns_current_user(self, client):
        register(client)
        tokens = client.post(reverse("login"), {"email": "neha@example.com", "password": PASSWORD}, format="json").data
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        res = client.get(reverse("me"))
        assert res.status_code == 200
        assert res.data["email"] == "neha@example.com"
        assert res.data["role"] == "candidate"


class TestRolePermissions:
    @staticmethod
    def request_for(role):
        user = User.objects.create_user(f"{role}@example.com", PASSWORD, role=role)
        request = APIRequestFactory().get("/")
        request.user = user
        return request

    def test_each_role_passes_only_its_own_check(self):
        for role, allowed in [(Role.CANDIDATE, IsCandidate), (Role.EMPLOYER, IsEmployer), (Role.ADMIN, IsAdminRole)]:
            request = self.request_for(role)
            for perm in (IsCandidate, IsEmployer, IsAdminRole):
                assert perm().has_permission(request, None) is (perm is allowed)

    def test_anonymous_fails_every_check(self):
        from django.contrib.auth.models import AnonymousUser

        request = APIRequestFactory().get("/")
        request.user = AnonymousUser()
        for perm in (IsCandidate, IsEmployer, IsAdminRole):
            assert perm().has_permission(request, None) is False
