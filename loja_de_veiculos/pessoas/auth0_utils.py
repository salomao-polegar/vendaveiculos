# api/auth0_utils.py

import requests

AUTH0_DOMAIN = 'dev-altixh64hogp2eea.us.auth0.com'
AUTH0_CLIENT_ID = 'xHiWjHYKqm1Aznsu9XwxmxcT57ZSM94v'
AUTH0_CLIENT_SECRET = 'Hl0juWCoND30xumwU45T-gDXF26GnpIzTockeb5RcuX4XnlCXfrIhnLr9f7pUfC_'
AUTH0_CONNECTION = 'Username-Password-Authentication'

def get_auth0_management_token():
    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
        "grant_type": "client_credentials"
    }
    res = requests.post(url, json=payload)
    res.raise_for_status()
    return res.json()["access_token"]
