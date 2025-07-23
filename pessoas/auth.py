from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from jose import jwt
from .auth0_utils import *
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import redirect

import requests

class Auth0User:
    def __init__(self, payload):
        self.payload = payload
        self.email = payload.get("email")
        self.sub = payload.get("sub")
        self.is_authenticated = True

    def __str__(self):
        return self.email or self.sub
    
class Auth0JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return None

        token = auth.split("Bearer ")[1]

        try:
            jwks = requests.get(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json').json()
            unverified_header = jwt.get_unverified_header(token)

            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"],
                    }

            if not rsa_key:
                raise AuthenticationFailed("Chave pública não encontrada.")

            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=AUTH0_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/"
            )

        except Exception as e:
            raise AuthenticationFailed(f"Token inválido: {str(e)}")

        user = Auth0User(payload)
        return user, token
    

def get_userinfo(request):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        raise Exception("Token não enviado")

    token = auth_header.split(' ')[1]
    url = f'https://{AUTH0_DOMAIN}/userinfo'
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Erro ao buscar userinfo")
    
class IsAdminEmail(BasePermission):
    def has_permission(self, request, _):
        admins = ['admin@lojaveiculos.com.br']
        try:
            userinfo = get_userinfo(request)
            email = userinfo.get("email", "").lower()
            return email in admins

        except Exception:
            return False