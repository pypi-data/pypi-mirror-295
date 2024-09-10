import datetime
import os
import requests

from logging import getLogger
from escherauth.escherauth import EscherRequestsAuth

from panoptica_genai_protection.auth_interface import MarvinAuthInterface
from panoptica_genai_protection.settings import SIGN_URL, SCOPE, ESCHER_TOKEN_URL, JWT_TIMEOUT_MS, DEFAULT_AUTH_HOST

logger = getLogger("marvin_auth")


class GenAIProtectionAuthException(Exception):
    def __init__(self, message):
        super().__init__(message)
        logger.error(message)


class GenAIProtectionAuth(MarvinAuthInterface):
    _instance = None

    @classmethod
    def get_instance(cls, access_key=None, secret_key=None, host=None,
                     sign_url=SIGN_URL, scope=SCOPE,
                     expiration_interval=JWT_TIMEOUT_MS):
        access_key = access_key if access_key else os.getenv("GENAI_PROTECTION_ACCESS_KEY")
        secret_key = secret_key if secret_key else os.getenv("GENAI_PROTECTION_SECRET_KEY")
        host = host if host else os.getenv("GENAI_PROTECTION_AUTH_HOST", DEFAULT_AUTH_HOST)
        if not access_key or not secret_key or not host:
            raise ValueError(
                'please provide valid GENAI_PROTECTION_ACCESS_KEY, GENAI_PROTECTION_SECRET_KEY, and GENAI_PROTECTION_AUTH_HOST')

        if cls._instance is None:
            cls._instance = cls(access_key, secret_key, host, sign_url, scope, expiration_interval)
        elif cls._instance._access_key != access_key or cls._instance._secret_key != secret_key or cls._instance._host != host:
            del cls._instance
            cls._instance = cls(access_key, secret_key, host, sign_url, scope, expiration_interval)
        return cls._instance

    def __init__(self, access_key, secret_key, host,
                 sign_url=SIGN_URL, scope=SCOPE, expiration_interval=JWT_TIMEOUT_MS):
        self._access_key = access_key
        self._secret_key = secret_key
        self._scope = scope
        self._host = host
        self._signurl = f"{host}{sign_url}"
        self._expires_at = 0
        self._expiration_interval = expiration_interval
        self._jwt = None

    def get_token(self):
        if datetime.datetime.utcnow().timestamp() < self._expires_at:
            return self._jwt
        signed_resp = requests.get(self._signurl,
                                   auth=EscherRequestsAuth(self._scope,
                                                           {'hash_algo': 'SHA512',
                                                            'auth_header_name': 'X-HMAC-Sign',
                                                            'date_header_name': 'X-HMAC-Date',
                                                            'algo_prefix': 'MRV'},
                                                           {'api_key': self._access_key,
                                                            'api_secret': self._secret_key}))
        if not signed_resp.ok:
            raise GenAIProtectionAuthException(signed_resp.text)
        resp = signed_resp.json()
        self._expires_at = datetime.datetime.utcnow().timestamp() + self._expiration_interval
        self._jwt = resp['token']
        return self._jwt

    def init_expired(self):
        self._expires_at = 0

    def get_headers(self):
        return {"Authorization": "Bearer " + self.get_token()}
