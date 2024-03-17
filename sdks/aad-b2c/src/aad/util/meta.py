from pydantic import BaseModel
import aiohttp

def metadata_url(tenant: str, policy: str):
    """
    - `tenant`: `"{tenant}.b2clogin.com/{tenant}..."`
    - `policy`: user flow name
    """
    return f"https://{tenant}.b2clogin.com/{tenant}.onmicrosoft.com/{policy}/v2.0/.well-known/openid-configuration"

class Meta(BaseModel):
    jwks_uri: str
    issuer: str

async def metadata(tenant: str, policy: str) -> Meta:
    async with aiohttp.ClientSession() as ses:
        async with ses.get(metadata_url(tenant, policy)) as r:
            return Meta.model_validate(await r.json())

