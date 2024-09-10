import re
from pathlib import Path
from typing import Optional, Union
from urllib.parse import quote_plus


class DatabaseUrlError(Exception): ...


class InvalidEngine(DatabaseUrlError): ...


def should_quote(value: str) -> bool:
    return not re.match(r"[-%\w]+$", value)


def generate(
    name: Union[Path, str, None] = "db.sqlite3",
    engine: str = "sqlite",
    host: Optional[str] = None,
    user: Optional[str] = None,
    password: Optional[str] = None,
    port: Union[str, int, None] = None,
    **extras,
) -> str:
    if engine == "sqlite" or (engine := engine.split(".")[-1]) in ("sqlite", "sqlite3"):
        if name is None:
            name = ":memory:"
        return f"sqlite://{name}"
    if (engine := engine.replace("postgresql", "postgres")) in (
        "postgres",
        "asyncpg",
        "psycopg",
    ):
        default_user = "postgres"
        default_port = 5432
        default_pw = "postgres"
    elif engine in ("mysql", "mariadb"):
        default_user = "root"
        default_port = 3306
        default_pw = "123456"
    elif engine == "mssql":
        default_user = "sa"
        default_port = 1432
        default_pw = "Abcd12345678"
    elif engine == "oracle":
        default_user = "SYSTEM"
        default_port = 1521
        default_pw = "123456"
    else:
        raise InvalidEngine(engine)
    if port is None:
        port = default_port
    if host is None:
        host = "127.0.0.1"
    if user is None:
        user = default_user
    if password is None:
        password = default_pw
    elif should_quote(password):
        password = quote_plus(password)
    url = f"{engine}://{user}:{password}@{host}:{port}/{name}"
    if extras:
        url += "?" + "&".join(f"{k}={v}" for k, v in extras.items())
    return url


def from_django_item(default: dict) -> str:
    return generate(**{k.lower(): v for k, v in default.items()})
