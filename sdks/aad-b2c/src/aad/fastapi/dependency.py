from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .. import authorize


def bearer(credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]) -> str:
    return credentials.credentials
Token = Annotated[str, Depends(bearer)]
    
def claims(tenant: str, app_id: str, policy: str) -> type[dict[str, str]]:
    """Returns a FastAPI dependency to authorize a JWT and return its claims
    - Raises `403 Forbidden` if there's no `"Authorization": "Bearer <token>"` header
    - Raises `401 Unauthorized` if the token is invalid
    
    Usage: 
    ```
    Claims = claims(tenant, app_id, policy)
    
    @app.get(...)
    def route(claims: Claims):
        ...
    ```
    """
    async def _claims(token: Token) -> dict[str, str]:
        try:
            return await authorize(token=token, tenant=tenant, app_id=app_id, policy=policy)
        except:
            raise HTTPException(status_code=401, detail="Unauthorized")
    
    return Annotated[dict[str, str], Depends(_claims)]