import base64
import hashlib
import hmac
import string
import random
import boto3
import requests
import time

from jose import jwk, jwt
from jose.utils import base64url_decode
from botocore.exceptions import ClientError
from fastapi import HTTPException, status

from ..settings import settings


def generate_secure_password(length: int = 12) -> str:
    if length < 12:
        raise ValueError("Password length should be at least 12 characters.")

    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    symbols = "!@#$%^&*()-_"

    password = [
        random.choice(uppercase_letters),
        random.choice(lowercase_letters),
        random.choice(digits),
        random.choice(symbols)
    ]

    all_characters = uppercase_letters + lowercase_letters + digits + symbols
    password += random.choices(all_characters, k=length - 4)

    random.shuffle(password)

    return ''.join(password)


class AWSCognitoService:
    def __init__(self):
        self.region = settings.AWS_COGNITO_REGION
        self.user_pool_id = settings.AWS_COGNITO_USER_POOL_ID
        self.app_client_id = settings.AWS_COGNITO_APP_CLIENT_ID
        self.app_client_secret = settings.AWS_COGNITO_APP_CLIENT_SECRET
        self.keys_url = f'https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json'
        self.jwks = self._get_jwks()
        self.client = boto3.client('cognito-idp', region_name=self.region)

    def _get_jwks(self):
        response = requests.get(self.keys_url)
        response.raise_for_status()
        return response.json()['keys']

    def verify_token(self, token: str):
        header = jwt.get_unverified_header(token)
        kid = header['kid']

        key_index = -1
        for i in range(len(self.jwks)):
            if kid == self.jwks[i]['kid']:
                key_index = i
                break
        if key_index == -1:
            raise ValueError('Public key not found in jwks.json')

        public_key = jwk.construct(self.jwks[key_index])

        message, encoded_signature = str(token).rsplit('.', 1)
        decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))

        if not public_key.verify(message.encode("utf8"), decoded_signature):
            raise ValueError('Signature verification failed')

        claims = jwt.get_unverified_claims(token)

        if time.time() > claims['exp']:
            raise ValueError('Token is expired')

        return claims

    def get_user_data(self, token: str) -> dict:
        claims = self.verify_token(token)
        return {
            "username": claims.get("username"),
            "email": claims.get("email", None),
            "sub": claims.get("sub"),
            "roles": claims.get("cognito:groups", []),
        }

    def get_current_user(self, token: str):
        try:
            return self.get_user_data(token)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )

    def get_secret_hash(self, email: str):
        message = email + self.app_client_id
        dig = hmac.new(
            self.app_client_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256).digest()
        return base64.b64encode(dig).decode()

    def add_user(
            self,
            email: str,
            user_attributes: dict = None
    ) -> dict:
        try:
            attributes = [
                {"Name": "email", "Value": email},
                {"Name": "email_verified", "Value": "false"}
            ]

            if user_attributes:
                for key, value in user_attributes.items():
                    attributes.append({"Name": key, "Value": value})

            temporary_password = generate_secure_password()

            response = self.client.admin_create_user(
                UserPoolId=self.user_pool_id,
                Username=email,
                UserAttributes=attributes,
                TemporaryPassword=temporary_password,
                MessageAction='SUPPRESS',
                ClientMetadata={
                    'SECRET_HASH': self.get_secret_hash(email)
                }
            )

            self.client.admin_set_user_password(
                UserPoolId=self.user_pool_id,
                Username=email,
                Password=temporary_password,
                Permanent=True
            )

            self.client.admin_add_user_to_group(
                UserPoolId=self.user_pool_id,
                Username=email,
                GroupName='ROLE_PRACTICE'
            )

            return response

        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.response['Error']['Message']
            )


def get_aws_cognito() -> AWSCognitoService:
    yield AWSCognitoService()
