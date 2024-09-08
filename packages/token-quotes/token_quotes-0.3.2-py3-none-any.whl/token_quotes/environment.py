import os
from typing import Optional


def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    value = os.getenv(var_name, default)
    if value is None:
        raise ValueError(f"Environment variable {var_name} is not set and no default provided.")
    return value


COVALENT_API_KEY: str = get_env_variable("COVALENT_API_KEY")
