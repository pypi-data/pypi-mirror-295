import struct
from typing import Optional
from azure.identity import DefaultAzureCredential
import pandas as pd
from sqlalchemy import URL, Connection, Engine, create_engine
from sqlalchemy import text as sql_text

from msal_bearer.BearerAuth import BearerAuth, get_user_name

_engine = None
_token = ""
_conn_string = ""
_user_name = ""


def set_token(token: str) -> None:
    """Setter for global property token.

    Args:
        token (str): Token to set.
    """
    global _token
    _token = token


def get_token() -> str:
    """Getter for token. Will first see if a global token has been set, then try to get a token using app registration, then last try to get via azure authentication.

    Returns:
        str: Authentication token
    """
    if _token:
        return _token

    app_token = get_app_token()
    if app_token:
        return app_token

    return get_az_token()


def reset_engine() -> None:
    """Reset cached Engine"""
    global _engine

    if _engine is not None:
        _engine.dispose()
        _engine = None


def get_engine(conn_string="", token="", reset=False) -> Engine:
    """Getter of cached Engine. Will create one if not existing.

    Args:
        conn_string (str, optional): Connection string for odbc connection. Defaults to "" to support just getting cached engine.
        token (str, optional): Token string. Defaults to "" to support just getting cached engine.
        reset (bool, optional): Set true to reset engine, i.e., not get cached engine. Defaults to False.
    """

    def get_token_struct(token: str) -> bytes:
        """Convert token string to token byte struct for use in connection string

        Args:
            token (str): Token as string

        Returns:
            (bytes): Token as bytes
        """
        tokenb = bytes(token, "UTF-8")
        exptoken = b""
        for i in tokenb:
            exptoken += bytes({i})
            exptoken += bytes(1)

        tokenstruct = struct.pack("=i", len(exptoken)) + exptoken

        return tokenstruct

    global _engine

    if not conn_string == _conn_string:
        reset = True

    if token == "":
        token = get_token()

    if reset:
        reset_engine()

    if _engine is None and isinstance(conn_string, str) and len(conn_string) > 0:
        SQL_COPT_SS_ACCESS_TOKEN = 1256
        _engine = create_engine(
            URL.create("mssql+pyodbc", query={"odbc_connect": conn_string}),
            connect_args={
                "attrs_before": {SQL_COPT_SS_ACCESS_TOKEN: get_token_struct(token)}
            },
        )

    return _engine


def get_sql_driver() -> str:
    """Get name of ODBC SQL driver

    Raises:
        ValueError: Raised if required ODBC driver is not installed.

    Returns:
        str: ODBC driver name
    """
    import pyodbc

    drivers = pyodbc.drivers()

    for driver in drivers:
        if "18" in driver and "SQL Server" in driver:
            return driver

    for driver in drivers:
        if "17" in driver and "SQL Server" in driver:
            return driver

    raise ValueError("ODBC driver 17 or 18 for SQL server is required.")


def get_connection_string(
    server: str, database: str, driver: str = get_sql_driver()
) -> str:
    """Build database connection string

    Args:
        server (str): Server url
        database (str): Database name
        driver (str): ODBC driver name. Defaults to get_sql_driver().

    Returns:
        str: Database connection string
    """
    return f"DRIVER={driver};SERVER={server};DATABASE={database};"


def get_az_token() -> str:
    """Getter for token uzing azure authentication.

    Returns:
        str: Token from azure authentication
    """
    credential = DefaultAzureCredential()
    databaseToken = credential.get_token("https://database.windows.net/")
    return databaseToken[0]


def get_app_token(username: str = "") -> str:
    """Getter for token using app registration authentication.

    Args:
        username (str, optional): User name (email address) of user to get token for.

    Returns:
        str: Token from app registration
    """
    global _user_name

    if not username:
        if not _user_name:
            _user_name = get_user_name()
        username = _user_name
    else:
        _user_name = username

    # SHORTNAME@equinor.com -- short name shall be capitalized
    username = username.upper()  # Also capitalize equinor.com
    if not username.endswith("@EQUINOR.COM"):
        username = username + "@EQUINOR.COM"

    tenantID = "3aa4a235-b6e2-48d5-9195-7fcf05b459b0"
    clientID = "5850cfaf-0427-4e96-9813-a7874c8324ae"
    scope = ["https://database.windows.net/.default"]
    auth = BearerAuth.get_auth(
        tenantID=tenantID, clientID=clientID, scopes=scope, username=username
    )
    return auth.token


def get_connection(database: str = "Lh_Gold", token: str = "") -> Connection:
    """Get Connection object to database.

    Args:
        database (str, optional): Name of database. Defaults to "Lh_Gold".
        token (str, optional): Token string. Defaults to get_token().

    Returns:
        Connection: Connection object to database
    """
    if not token:
        token = get_token()

    server = "gwrkioxcw3kuremvp7hqlnczwa-bjb35lhdq4oubeecgujfxwyxcu.datawarehouse.fabric.microsoft.com"

    return get_engine(
        get_connection_string(server=server, database=database), token
    ).connect()


def query(
    sql: str,
    connection: Optional[Connection] = None,
    params: Optional[dict] = None,
) -> pd.DataFrame:
    """Query SQL database using pd.read_sql

    Args:
        sql (str): SQL query for database
        connection (Optional[Connection], optional): Database Connection object. Defaults to None, which resolves to get_connection().
        params (Optional[dict], optional): SQL parameters. Defaults to None.

    Returns:
        pd.DataFrame: Result from pd.read_sql
    """
    if connection is None:
        connection = get_connection()

    return pd.read_sql(sql_text(sql), connection, params=params)
