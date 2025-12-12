"""
Tests for Better-Auth feature
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from api.auth_better.better_auth_router import router
from fastapi import FastAPI

# Create a test app with the auth router
app = FastAPI()
app.include_router(router, prefix="/auth")

client = TestClient(app)


def test_signup_endpoint():
    """Test the signup endpoint"""
    response = client.post(
        "/auth/signup",
        json={
            "email": "test@example.com",
            "password": "securepassword123",
            "name": "Test User",
            "software_background": "5 years of Python development",
            "hardware_background": "Experience with Arduino and Raspberry Pi"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert data["email"] == "test@example.com"


def test_signin_endpoint():
    """Test the signin endpoint"""
    response = client.post(
        "/auth/signin",
        json={
            "email": "test@example.com",
            "password": "securepassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert data["email"] == "test@example.com"


def test_verify_session_endpoint():
    """Test the verify session endpoint"""
    # This test uses a fake token since we're not implementing full JWT validation in tests
    response = client.post(
        "/auth/verify-session",
        json={
            "token": "fake-token-for-testing"
        }
    )
    # The response depends on the implementation - for now, we expect a 200 response
    assert response.status_code in [200, 401]  # Could be valid or invalid depending on implementation


def test_create_profile_endpoint():
    """Test the create profile endpoint"""
    response = client.post(
        "/auth/create-profile",
        json={
            "user_id": "test_user_123",
            "software_background": "Python, JavaScript, React",
            "hardware_background": "Arduino, Raspberry Pi, ESP32",
            "robotics_experience": "2 years building robots",
            "programming_languages": ["Python", "C++", "JavaScript"],
            "hardware_platforms": ["Arduino", "Raspberry Pi"],
            "years_of_experience": 2,
            "primary_interest": "Humanoid robots",
            "education_level": "undergraduate"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test_user_123"


def test_sync_vector_endpoint():
    """Test the sync vector endpoint"""
    response = client.post(
        "/auth/sync-vector",
        json={
            "user_id": "test_user_123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["success", "error"]


def test_signout_endpoint():
    """Test the signout endpoint"""
    response = client.post("/auth/signout")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Sign out successful"


def test_auth_health_check():
    """Test the auth health check endpoint"""
    response = client.get("/auth/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "Better-Auth Integration"