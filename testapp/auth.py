import jwt
from rest_framework import authentication, exceptions
from .models import *



class JWTAuthenticationCustomer(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)

        if auth_data == b'':
            raise exceptions.AuthenticationFailed('Please provide the token,login')

        token = auth_data.decode('utf-8')
        try:
            payload = jwt.decode(token, 'secret')
            try:
                user =UserProfile.objects.get(id=payload['user'])
                return (user, token)
            except UserProfile.DoesNotExist:raise exceptions.AuthenticationFailed('Your token is invalid,login')
        # print(payload)

        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed('Your token is invalid,login')
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed('Your token is expired,login')
