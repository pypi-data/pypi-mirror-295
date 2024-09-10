import os
import httpx
from fastapi import HTTPException
from chainlit.user import User
from chainlit.oauth_providers import OAuthProvider
from fief_client import FiefAsync


class FiefOAuthProvider(OAuthProvider):
    id = "botrun"
    env = [
        "FIEF_CLIENT_ID",
        "FIEF_CLIENT_SECRET",
        "FIEF_BASE_URL",
        "FIEF_REDIRECT_URI",
    ]

    def __init__(self):
        self.client_id = os.getenv("FIEF_CLIENT_ID", "")
        self.client_secret = os.getenv("FIEF_CLIENT_SECRET", "")
        self.base_url = os.getenv("FIEF_BASE_URL", "")
        self.redirect_uri = os.getenv("FIEF_REDIRECT_URI", "")
        self.fief_client = FiefAsync(
            self.base_url,
            self.client_id,
            self.client_secret,
        )
        self.authorize_params = {
            "response_type": "code",
            "scope": "openid profile email",
        }
        self.authorize_url = f"{self.base_url}/authorize"

    async def get_token(self, code: str, url: str) -> str:
        tokens, _ = await self.fief_client.auth_callback(code, self.redirect_uri)
        return tokens["access_token"]

    async def get_user_info(self, token: str):
        userinfo = await self.fief_client.userinfo(token)
        # print(f"[FiefOAuthProvider][get_user_info] userinfo: {userinfo}")
        display_name = userinfo.get("fields", {}).get("unit", userinfo["email"])
        user = User(
            identifier=userinfo["sub"],
            display_name=display_name,
            metadata={
                "provider": "fief",
                "email": userinfo.get("email"),
                "name": userinfo.get("name"),
            },
        )
        return userinfo, user
