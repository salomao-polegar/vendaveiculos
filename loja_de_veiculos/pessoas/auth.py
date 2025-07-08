import json
from urllib.request import urlopen
from jose import jwt
from rest_framework import authentication, exceptions

AUTH0_DOMAIN = 'https://dev-altixh64hogp2eea.us.auth0.com'
API_AUDIENCE = 'https://veiculosapi.example.com'
ALGORITHMS = ['RS256']

class Auth0JSONWebTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return None

        parts = auth.split()
        if parts[0].lower() != 'bearer':
            raise exceptions.AuthenticationFailed('Authorization header must start with Bearer')
        elif len(parts) == 1:
            raise exceptions.AuthenticationFailed('Token not found')
        elif len(parts) > 2:
            raise exceptions.AuthenticationFailed('Authorization header must be Bearer token')

        token = parts[1]
        try:
            jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
            jwks = json.loads(jsonurl.read())
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}
            for key in jwks['keys']:
                if key['kid'] == unverified_header['kid']:
                    rsa_key = {
                        'kty': key['kty'],
                        'kid': key['kid'],
                        'use': key['use'],
                        'n': key['n'],
                        'e': key['e']
                    }
            if rsa_key:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer=f'https://{AUTH0_DOMAIN}/'
                )
            else:
                raise exceptions.AuthenticationFailed('Unable to find appropriate key')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expired')
        except jwt.JWTClaimsError:
            raise exceptions.AuthenticationFailed('Incorrect claims')
        except Exception:
            raise exceptions.AuthenticationFailed('Unable to parse authentication token')

        # Aqui você pode criar ou obter um usuário Django
        from django.contrib.auth.models import AnonymousUser
        # Para simplificar, retorna AnonymousUser e o payload
        return (AnonymousUser(), payload)
