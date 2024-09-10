from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import logging

logging.basicConfig(level=logging.DEBUG)


class AuthHandler:
    def __init__(self, auth_token):
        self.auth_token = auth_token

    is_using_auth = False
    security = HTTPBearer()
    optional_security = HTTPBearer(auto_error=False)

    def __check_access_token__(self, token) -> str:
        if token == self.auth_token:
            return "success"
        else:
            raise HTTPException(status_code=401, detail="invalid token")

    def auth_wrapper(
        self,
        auth: HTTPAuthorizationCredentials = Security(
            security if is_using_auth else optional_security
        ),
    ):
        if self.is_using_auth:
            if auth is None:
                raise HTTPException(status_code=401, detail="not authenticated")
            return self.__check_access_token__(auth.credentials)
        else:
            return "success"
