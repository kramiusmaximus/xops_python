from os import getenv


def _getenv(var_name: str) -> str:
    var = getenv(var_name)
    if var is None:
        raise Exception("Config var missing")
    return var


DB_URL = _getenv("DB_URL")
