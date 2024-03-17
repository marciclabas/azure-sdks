# Azure AD B2C

> Simplified Python SDK for verifying AD B2C-issued JWTs

## Usage

```python
import aad

token = "..." # JWT to verify
tenant = "..." # B2C tenant (as in `"{tenant}.b2clogin.com/{tenant}..."`)
app_id = "..." # ClientID of app registered in the B2C tenant
policy = "B2C_1_..." # policy (aka user flow) name

await aad.authorize(token, tenant, app_id, policy)
# {
#   "idp": "...",
#   "aud": "...",
#   ... # other JWT fields
#   ... # fields configured in B2C
# }
```

## FastAPI dependency

```bash
pip install aad[fastapi]
```

```python
from fastapi import FastAPI
import aad

Claims = aad.claims(tenant, app_id, policy)
app = FastAPI()

@app.get("...")
def get(claims: Claims):
    ...
```

## Disclaimer

The JWT decoding part is heavily inspired by [azure-ad-verify-token](https://pypi.org/project/azure-ad-verify-token/), but with an async interface