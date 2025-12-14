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
###