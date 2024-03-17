# adapted from https://pypi.org/project/azure-ad-verify-token/
import base64
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

def ensure_bytes(key: str) -> bytes:
    if isinstance(key, str):
        key = key.encode('utf-8')
    return key

def decode_value(val: str) -> int:
    decoded = base64.urlsafe_b64decode(ensure_bytes(val) + b'==')
    return int.from_bytes(decoded, 'big')

def rsa_pem(n: str, e: str) -> bytes:
    return RSAPublicNumbers(
        n=decode_value(n),
        e=decode_value(e)
    ).public_key(default_backend()).public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
