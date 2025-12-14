import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


def get_config(key: str, default: Optional[str] = None) -> Optional[str]:
    return os.getenv(key, default)


### DEFAULT SETTINGS
POSTGRES_USER = get_config(key="POSTGRES_USER", default="user")
POSTGRES_PASSWORD = get_config(key="POSTGRES_PASSWORD", default="password")
POSTGRES_DB = get_config(key="POSTGRES_DB", default="database")
POSTGRES_PORT = get_config(key="POSTGRES_PORT", default="5432")
###

# JWT SETTINGS
JWT_SECRET = get_config(key="JWT_SECRET", default="change-this-secret-in-prod")
# Use HS256 Hashing Algorithm
JWT_ALGORITHM = get_config(key="JWT_ALGORITHM", default="HS256")
# Token expiration in 1 hour
try:
    JWT_EXP_SECONDS = int(get_config(key="JWT_EXP_SECONDS", default="3600"))
except Exception:
    JWT_EXP_SECONDS = 3600
