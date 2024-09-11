from fastapi import Depends

from ..utils.aws_cognito import AWSCognitoService, get_aws_cognito
from ..dto import UserDTO
from ..utils.bearer import get_token


def require_user(
        token: str = Depends(get_token),
        cognito_service: AWSCognitoService = Depends(get_aws_cognito)
) -> UserDTO:
    return UserDTO(**cognito_service.get_current_user(token))
