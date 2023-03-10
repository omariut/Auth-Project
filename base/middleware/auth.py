import json
from typing import Dict, List, Union

from django.http import HttpRequest, JsonResponse
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from config.settings import SECRET_KEY
from user.models import User
from user.token import get_user
from base.decorator_exception_handler import exception_handler


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    
    def get_user(request,token: str) -> Union[User, object]:
        try:
            try:
                user_data = get_user(token)
        
            except Exception:
                raise ValidationError(detail='user data not found', code=401)
            user = User.objects.get(username__exact=user_data['username'])
            if not user.is_active or not user.verified:
                return
            return user
        except User.DoesNotExist:
            return
    
    def __call__(self, request: HttpRequest):
        auth_header: str = request.headers.get('authorization')
        if auth_header:
            token_obj: List[str] = auth_header.split(' ')
            if token_obj[0].lower() != 'bearer':
                return JsonResponse(data={
                    'message': 'invalid token type',
                    'success': False,
                }, status=400)
            try:
                user_obj = self.get_user(request, token=token_obj[1])
                if not user_obj:
                    return JsonResponse(data={
                        'message': 'cannot retrieve user information',
                        'success': False
                    }, status=401)
                setattr(request, 'user', user_obj)
            except Exception as err:
                return JsonResponse(data={
                    'message': 'user data not found',
                    'success': False,

                    
                }, status=401)
        response = self.get_response(request)
        return response
