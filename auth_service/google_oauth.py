# auth_service/google_oauth.py

import requests
from urllib.parse import urlencode

# --------------------------------------------
# CONFIG — REPLACE WITH YOUR GOOGLE CREDENTIALS
# --------------------------------------------
GOOGLE_CLIENT_ID = "335419054496-2edomcmaa92oohvc4m6gn905eq5e20ai.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"

# This must match what you configured in Google Cloud Console
REDIRECT_URI = "http://localhost:8001/auth/callback"

# Google OAuth URLs
GOOGLE_AUTH_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


def get_google_login_url() -> str:
    """
    Returns the Google OAuth URL where the user should be redirected.
    """

    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }

    return f"{GOOGLE_AUTH_BASE_URL}?{urlencode(params)}"


def get_google_access_token(code: str) -> str:
    """
    Exchange authorization code for access token.
    """

    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    response = requests.post(GOOGLE_TOKEN_URL, data=data)
    token_data = response.json()

    if "access_token" not in token_data:
        raise Exception(f"Google token error: {token_data}")

    return token_data["access_token"]


def get_google_user_info(code: str) -> dict:
    """
    Uses the authorization code to get the user's Google profile (email, name, etc.).
    """

    # Step 1 — Get access token
    access_token = get_google_access_token(code)

    # Step 2 — Get user info
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
    user_info = response.json()

    if "email" not in user_info:
        raise Exception(f"Failed to fetch email: {user_info}")

    return user_info
