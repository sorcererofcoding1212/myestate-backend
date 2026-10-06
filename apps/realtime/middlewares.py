from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

Account = get_user_model()


class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()

        query_params = parse_qs(query_string)

        access_token = query_params.get("access", [None])[0]

        if access_token:
            token = AccessToken(access_token)
            user = await Account.objects.aget(id=token["user_id"])
            scope["user"] = user

        return await self.app(scope, receive, send)
