import time
from typing import Dict

import fastapi
import jwt
from fastapi import HTTPException, status
from pydantic import BaseModel

from settings import JWT_SECRET, JWT_ALGORITHM, JWT_EXP_SECONDS

router = fastapi.APIRouter()


class TokenRequest(BaseModel):
    username: str = "user"
    password: str = "password"


@router.post("/auth/token")
async def login(payload: TokenRequest):
    """
    For simplicity, accept a single hardcoded username/password and return a JWT.
    """
    # Hardcoded user check (do not change auth design)
    if payload.username != "user" or payload.password != "password":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    now = int(time.time())
    exp = now + JWT_EXP_SECONDS
    claims: Dict[str, object] = {"sub": payload.username, "iat": now, "exp": exp}

    try:
        token = jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Token generation failed") from exc

    return {"access_token": token, "token_type": "bearer", "expires_in": JWT_EXP_SECONDS}
