import json
import secrets
from django.core.cache import cache
from user.serializers import UserTokenSerializer

def get_token(user):
    token=secrets.token_hex(16)
    cache.set(key=token, value=json.dumps(UserTokenSerializer(user).data), timeout=5*60*60)
    return token

def get_user(token):
    user_data = json.loads(cache.get(token))
    return user_data
