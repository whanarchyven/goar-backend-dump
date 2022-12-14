from channels.db import database_sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication


@database_sync_to_async
def get_user(token):
    jwt = JWTAuthentication()
    return jwt.get_user(jwt.get_validated_token(token))


class QueryAuthMiddleware:
    """
    Custom middleware (insecure) that takes user IDs from the query string.
    """

    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app

    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        scope['user'] = await get_user(scope['query_string'])

        return await self.app(scope, receive, send)
