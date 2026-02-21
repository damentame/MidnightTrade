from urllib.parse import urlencode

from app.config import settings


AUTH_BASE = "https://id.ctrader.com/my/settings/openapi/grantingaccess/"


def get_auth_url(state: str) -> str:
    params = {
        "client_id": settings.ctrader_client_id,
        "redirect_uri": settings.ctrader_redirect_uri,
        "scope": "trading",
        "state": state,
        "response_type": "code",
    }
    return f"{AUTH_BASE}?{urlencode(params)}"


def exchange_code_for_token(code: str) -> dict:
    return {
        "access_token": f"mock_access_{code}",
        "refresh_token": f"mock_refresh_{code}",
        "token_type": "bearer",
    }
